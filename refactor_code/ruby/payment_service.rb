require 'faraday'

class PaymentService
  class << self
    CARD_PAYMENT_API = 'http://paymentmock/api/card'
    POYJP_PAYMENT_API = 'http://paymentmock/api/poyjp'
    BANK_PAYMENT_API = 'http://paymentmock/api/bank'

    def card_payment(card_number, price)
      res = Faraday.post(CARD_PAYMENT_API, JSON.generate({
                           card_number: card_number,
                           price: price
                         }), content_type: "application/json")
      return JSON.parse(res.body)["success"]
    end

    def poyjp_payment(account_number, price)
      res = Faraday.post(POYJP_PAYMENT_API, JSON.generate({
                           account_number: account_number,
                           price: price
                         }), content_type: "application/json")
      return JSON.parse(res.body)["success"]
    end

    def bank_payment(branch_number, account_number, price)
      res = Faraday.post(BANK_PAYMENT_API, JSON.generate({
                           branch_number: branch_number,
                           account_number: account_number,
                           price: price
                         }), content_type: "application/json")
      return JSON.parse(res.body)["success"]
    end
  end
end
