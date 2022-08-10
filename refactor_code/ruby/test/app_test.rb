ENV['RACK_ENV'] = 'test'
ENV["SINATRA_ENV"] = "test"

require './app'
require './test/test_helper'

def app
  Sinatra::Application
end

describe "/" do
  it "index" do
    get '/'
    _(last_response).must_be_ok
    _(last_response.body).must_include 'tea_0'
    _(last_response.body).must_include 'tea_1'
    _(last_response.body).must_include 'tea_2'
  end

  it "search" do
    get '/?q=tea_0'
    _(last_response).must_be_ok
    _(last_response.body).must_include 'tea_0'
  end
end

describe "/users/new" do
  it do
    get '/users/new'
    _(last_response).must_be_ok
    _(last_response.body).must_include 'username'
  end
end


describe "/login" do
  it do
    get '/login'
    _(last_response).must_be_ok
    _(last_response.body).must_include 'username'
  end
end

describe "/settle" do
  it do
    get '/settle'
    _(last_response).must_be_ok
  end
end

describe "signup and login scenario" do
  it do
    post '/users', {login: 'denzow', email: 'denzow@example.com', password: 'denzow_pass'}
    _(last_response.status).must_equal 302

    get 'logout'
    _(last_response.status).must_equal 302

    post '/login', {login: 'denzow', password: 'denzow_pass'}
    _(last_response.status).must_equal 302

    post '/login', {login: 'invalid', password: 'invalid'}
    _(last_response).must_be_ok
    _(last_response.body).must_include 'Invalid username or password'
  end
end

describe "buy tea scenario" do
  it do
    post '/users', {login: 'h3poteto', email: 'h3poteto@example.com', password: 'h3poteto_pass'}
    _(last_response.status).must_equal 302

    post '/cart', {teaId: '2', teaAmount: '200'}
    _(last_response.status).must_equal 302
    get '/'
    _(last_response.body).must_include 'Sold'

    get '/cart'
    _(last_response).must_be_ok
    _(last_response.body).must_include 'tea_1'
    _(last_response.body).must_include '200'

    get '/checkout'
    _(last_response).must_be_ok
    _(last_response.body).must_include '4380 yen'

    post '/buy', {paymentType: 'poyjp', paymentInfo1: '123456789'}
    _(last_response.status).must_equal 302
    get '/'
    _(last_response.body).must_include 'Teas.'
  end
end
