ActiveRecord::Base.connection.execute("DELETE FROM teas")
ActiveRecord::Base.connection.execute("DELETE FROM carts")
ActiveRecord::Base.connection.execute("DELETE FROM orders")
ActiveRecord::Base.connection.execute("DELETE FROM users")
ActiveRecord::Base.connection.execute("VACUUM")

User.create(login: 'testuser', email: 'testuser@example.com', password: 'testuser')
for i in 0..20 do
  Tea.create(
    name: "tea_#{i}",
    price: (10 + i % 3 * 10),
    stock_amount: (100 + i % 5 * 100),
    description: "description of #{i}"
  )
end
