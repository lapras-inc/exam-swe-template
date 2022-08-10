require 'minitest/autorun'
require "rack-minitest/test"
require 'database_cleaner'

ActiveRecord::Migration.maintain_test_schema!

DatabaseCleaner.strategy = :transaction

class Minitest::Spec
  before :each do
    DatabaseCleaner.start
  end

  after :each do
    DatabaseCleaner.clean
  end
end

