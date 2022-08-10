# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2018_11_06_042324) do
  create_table "carts", force: :cascade do |t|
    t.integer "user_id"
    t.text "teas_data", default: "--- {}\n"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["user_id"], name: "index_carts_on_user_id"
  end

  create_table "orders", force: :cascade do |t|
    t.integer "user_id"
    t.text "teas_data"
    t.text "payment_type", default: "card"
    t.text "payment_info"
    t.integer "status", default: 0
    t.integer "total_price"
    t.datetime "bought_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["user_id"], name: "index_orders_on_user_id"
  end

  create_table "teas", force: :cascade do |t|
    t.string "name", null: false
    t.integer "price", null: false
    t.text "description"
    t.integer "stock_amount", null: false
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

  create_table "users", force: :cascade do |t|
    t.string "login", null: false
    t.string "email", null: false
    t.string "crypted_password", null: false
    t.string "password_salt", null: false
    t.string "persistence_token"
    t.string "single_access_token"
    t.string "perishable_token"
    t.integer "login_count", default: 0, null: false
    t.integer "failed_login_count", default: 0, null: false
    t.datetime "last_request_at", precision: nil
    t.datetime "current_login_at", precision: nil
    t.datetime "last_login_at", precision: nil
    t.string "current_login_ip"
    t.string "last_login_ip"
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
  end

end
