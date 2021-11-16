class CreateOrders < ActiveRecord::Migration[5.2]
  def change
    create_table :orders do |t|
      t.references :user
      t.text :teas_data
      t.text :payment_type, default: 'card'
      t.text :payment_info, default: nil
      t.integer :status, default: 0
      t.integer :total_price
      t.datetime :bought_at
      t.timestamps null: false
    end
  end
end
