class CreateTeas < ActiveRecord::Migration[5.2]
  def change
    create_table :teas do |t|
      t.string :name, null: false
      t.integer :price, null: false
      t.text :description
      t.integer :stock_amount, null: false
      t.timestamps null: false
    end
  end
end
