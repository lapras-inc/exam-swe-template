class CreateCarts < ActiveRecord::Migration[5.2]
  def change
    create_table :carts do |t|
      t.references :user
      t.text :teas_data, default: {}.to_yaml
      t.timestamps null: false
    end
  end
end
