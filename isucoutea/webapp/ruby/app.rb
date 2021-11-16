require 'sinatra/base'
require 'mysql2'
require 'mysql2-cs-bind'
require 'erubis'

module Isucoutea
  class AuthenticationError < StandardError; end
  class PermissionDenied < StandardError; end
end

class Isucoutea::WebApp < Sinatra::Base
  TEAS_PER_PAGE = 6

  set :erb, escape_html: true
  set :public_folder, File.expand_path('../css', __FILE__)
  set :protection, true

  helpers do
    def config
      @config ||= {
        db: {
          host: 'localhost',
          port: 3306,
          username: 'scouty',
          password: 'scouty',
          database: 'scoutea'
        }
      }
    end

    def db
      return Thread.current[:isucoutea_db] if Thread.current[:isucoutea_db]
      client = Mysql2::Client.new(
        host: config[:db][:host],
        port: config[:db][:port],
        username: config[:db][:username],
        password: config[:db][:password],
        database: config[:db][:database],
        reconnect: true
      )
      client.query_options.merge!(symbolize_keys: true)
      Thread.current[:isucoutea_db] = client
      client
    end


    def get_country(tea)
      location_id = db.xquery('SELECT id FROM locations WHERE name = ?', tea[:location]).first[:id]
      country_id = db.xquery('SELECT location_to_id FROM location_relations WHERE location_from_id = ?',
                             location_id).first[:location_to_id]
      return db.xquery('SELECT name FROM locations WHERE id = ?', country_id).first[:name]
    end
  end

  get '/' do
    page = [(params[:page].to_i || 1), 1].max
    query = params[:query] || ''
    offset = (page - 1) * TEAS_PER_PAGE

    teas = db.xquery('SELECT * FROM teas ORDER BY id DESC')

    teas_match = []
    teas.each do |tea|
      if query == ''
        teas_match.push(tea)
        next
      end

      tea[:country] = get_country(tea)
      if query == tea[:name] || query == tea[:location] || query == tea[:country]
        teas_match.push(tea)
      end
    end

    teas_display = []
    teas_match.each_with_index do |tea, i|
      if offset <= i && i < offset + TEAS_PER_PAGE
        tea[:country] = get_country(tea)
        tea[:description] = tea[:description].length > 100 ? tea[:description][0, 100] + '...' : tea[:description]
        teas_display.push(tea)
      end
    end

    first_page = 1
    current_page = page
    last_page = (teas_match.length / (TEAS_PER_PAGE * 1.0)).ceil

    erb :index, locals: {
      teas: teas_display,
      query: query,
      url_query: query.empty? ? '' : '&query=' + query,
      first_page: first_page,
      current_page: current_page,
      last_page: last_page
    }
  end

  post '/' do
    name = params[:name]
    location = params[:location]
    description = params[:description]

    location_exist = db.xquery('SELECT 1 FROM locations WHERE name = ?', location)
    if location_exist
      db.xquery('INSERT INTO teas (name, location, description) VALUES (?, ?, ?)', name, location, description)
    end
    redirect '/'
  end

  get '/new' do
    erb :new, locals: {query: ''}
  end

  get '/initialize' do
    db.query('DELETE FROM teas WHERE id > 500000')
    db.query('DELETE FROM locations WHERE id > 2397')
    db.query('DELETE FROM location_relations WHERE id > 2394')
    redirect '/'
  end
end
