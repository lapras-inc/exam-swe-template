require 'active_support'
require 'sinatra'
require 'sinatra/reloader' if development?
require 'pry' if development?
require './models'
require './payment_service'

set :bind, '0.0.0.0'
enable :sessions

before '/cart' do
  redirect '/login' unless !!UserSession.find
end

before '/change_cart' do
  redirect '/login' unless !!UserSession.find
end

before '/checkout' do
  redirect '/login' unless !!UserSession.find
end

before '/buy' do
  redirect '/login' unless !!UserSession.find
end

before do
  if !!UserSession.find
    @current_user = UserSession.find.try(:user)
  end
end

get '/' do
  if @current_user
    cart = Cart.find_or_create_by(user: @current_user)
    @teas = cart.teas_data
  else
    @teas = {}
  end
  @query = params[:q]
  @tea_list = []
  if @query
    @tea_list = Tea.where('name like ? or description like ?', "%#{@query}%", "%#{@query}%").order('id')
  else
    @tea_list = Tea.all().order('id')
  end
  erb :index
end

get '/users/new' do
  @user = User.new
  erb :user_new
end

post '/users' do
  begin
    User.create!(symbolize_params.slice(:login, :email, :password))
    redirect '/'
  rescue ActiveRecord::RecordInvalid => e
    @error = e
    @user = e.record
    erb :user_new
  end
end

get '/login' do
  @session = UserSession.new
  erb :login
end

post '/login' do
  begin
    UserSession.create!(symbolize_params.slice(:login, :password))
    redirect '/'
  rescue Authlogic::Session::Existence::SessionInvalidError => e
    @error = 'Invalid username or password'
    erb :login
  end
end


get '/logout' do
  UserSession.find.try(:destroy)
  redirect '/login'
end

get '/teas/:id' do
  id = params[:id]
  @tea = Tea.find(id)
  erb :tea
end

get '/cart' do
  cart = Cart.find_or_create_by(user: @current_user)
  @cart_data = []
  cart.teas_data.each do |tea|
    @cart_data.append({
                       tea: Tea.find(tea[0].to_i),
                       amount: tea[1]
                     })
  end
  erb :cart
end

post '/cart' do
  cart = Cart.find_or_create_by(user: @current_user)
  teas = cart.teas_data
  tea_id = params[:teaId]
  tea_amount = params[:teaAmount].to_i
  unless teas[tea_id]
    teas[tea_id] = 0
  end
  teas[tea_id] += tea_amount
  cart.teas_data = teas
  cart.save!
  redirect '/'
end

post '/change_cart' do
  cart = Cart.find_by(user: @current_user)
  teas = cart.teas_data
  tea_id = params[:teaId]
  tea_amount = params[:teaAmount].to_i
  teas[tea_id] = tea_amount
  if tea_amount == 0
    teas.delete(tea_id)
  end
  cart.teas_data = teas
  cart.save!
  redirect '/cart'
end

get '/checkout' do
  cart = Cart.find_by(user: @current_user)
  teas = cart.teas_data
  @cart_data = []
  @total_price = 0
  @total_amount = 0
  teas.each do |data|
    tea = Tea.find(data[0].to_i)
    @cart_data.append({
                        tea: tea,
                        price: data[1] * tea.price
                      })
    @total_price += data[1] * tea.price
    @total_amount += data[1]
  end
  erb :checkout
end

post '/buy' do
  payment_type = params[:paymentType]
  payment_info_1 = params[:paymentInfo1]
  # optional
  payment_info_2 = params[:paymentInfo2]
  cart = Cart.find_by(user: @current_user)
  teas = cart.teas_data
  total_price = 0
  total_amount = 0
  ActiveRecord::Base.transaction do
    teas.each do |data|
      tea_id = data[0]
      amount = data[1]
      tea = Tea.find(tea_id.to_i)
      if tea.stock_amount < amount
        raise "Not enough amount for #{tea}"
      end
      tea.stock_amount -= amount
      tea.save!
      total_price += amount * tea.price
      total_amount += amount
    end

    total_price += total_price + 1.08 + (total_amount / 100 * 30)
    if payment_type != 'bank'
      Order.create(
        user: @current_user,
        teas_data: teas,
        payment_type: payment_type,
        payment_info: payment_info_1,
        total_price: total_price
      )
    else
      Order.create(
        user: @current_user,
        teas_data: teas,
        payment_type: payment_type,
        payment_info: {
          branch_number: payment_info_1,
          account_number: payment_info_2
        },
        total_price: total_price
      )
    end
    cart.delete
  end
  redirect '/'
end

# 定期的にバッチから叩かれ，決済処理をまとめて行う
get '/settle' do
  target_orders = Order.where(status: 0)
  is_success = true
  target_orders.each do |order|
    puts("target order #{order}")
    case order.payment_type
    when 'card' then
      result = PaymentService.card_payment(order.payment_info, order.total_price)
      if result
        order.status = 1
        order.payment_info = nil
        order.save
      else
        is_success = false
      end
    when 'poyjp' then
      result = PaymentService.poyjp_payment(order.payment_info, order.total_price)
      if result
        order.status = 1
        order.payment_info = nil
        order.save
      else
        is_success = false
      end
    when 'bank' then
      payment_info = order.payment_info
      result = PaymentService.bank_payment(payment_info[:branch_number], payment_info[:account_number], order.total_price)
      if result
        order.status = 1
        order.payment_info = nil
        order.save
      else
        is_success = false
      end
    end
  end
  {success: is_success}.to_json
end

def symbolize_params
  @normalized ||= params.deep_symbolize_keys!
end
