require './app'
require './test/test_helper'

def app
  Sinatra::Application
end

describe "/" do
  it "index" do
    get '/'
    last_response.must_be_ok
    last_response.body.must_include 'tea_0'
    last_response.body.must_include 'tea_1'
    last_response.body.must_include 'tea_2'
  end

  it "search" do
    get '/?q=tea_0'
    last_response.must_be_ok
    last_response.body.must_include 'tea_0'
  end
end

describe "/users/new" do
  it do
    get '/users/new'
    last_response.must_be_ok
    last_response.body.must_include 'username'
  end
end


describe "/login" do
  it do
    get '/login'
    last_response.must_be_ok
    last_response.body.must_include 'username'
  end
end

describe "/settle" do
  it do
    get '/settle'
    last_response.must_be_ok
  end
end

describe "signup and login scenario" do
  it do
    post '/users', {login: 'denzow', email: 'denzow@example.com', password: 'denzow_pass'}
    last_response.status.must_equal 302

    get 'logout'
    last_response.status.must_equal 302

    post '/login', {login: 'denzow', password: 'denzow_pass'}
    last_response.status.must_equal 302

    post '/login', {login: 'invalid', password: 'invalid'}
    last_response.must_be_ok
    last_response.body.must_include 'Invalid username or password'
  end
end

describe "buy tea scenario" do
  it do
    post '/users', {login: 'h3poteto', email: 'h3poteto@example.com', password: 'h3poteto_pass'}
    last_response.status.must_equal 302

    post '/cart', {teaId: '2', teaAmount: '200'}
    last_response.status.must_equal 302
    get '/'
    last_response.body.must_include 'Sold'

    get '/cart'
    last_response.must_be_ok
    last_response.body.must_include 'tea_1'
    last_response.body.must_include '200'

    get '/checkout'
    last_response.must_be_ok
    last_response.body.must_include '4380 yen'

    post '/buy', {paymentType: 'poyjp', paymentInfo1: '123456789'}
    last_response.status.must_equal 302
    get '/'
    last_response.body.must_include 'Teas.'
  end
end
