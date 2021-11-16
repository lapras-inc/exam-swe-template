class CreateUsers < ActiveRecord::Migration[5.2]
  def change
    create_table :users do |t|
      t.string :login, null: false
      t.string :email, null: false

      t.string :crypted_password, null: false
      t.string :password_salt, null: false

      t.string :persistence_token
      t.string :single_access_token
      t.string :perishable_token

      t.integer :login_count, default: 0, null: false
      t.integer :failed_login_count, default: 0, null: false
      t.datetime :last_request_at
      t.datetime :current_login_at
      t.datetime :last_login_at
      t.string :current_login_ip
      t.string :last_login_ip

      t.timestamps null: false
    end
  end
end
