require 'sinatra/activerecord'
require 'active_record'
require 'authlogic'

class User < ActiveRecord::Base
  acts_as_authentic do |config|
    config.login_field = :login
    config.require_password_confirmation = false
  end
end

class UserSession < Authlogic::Session::Base
end

class Tea < ActiveRecord::Base
end

class Cart < ActiveRecord::Base
  belongs_to :user
  serialize :teas_data
end

class Order < ActiveRecord::Base
  belongs_to :user
  serialize :teas_data
  serialize :payment_info
end
