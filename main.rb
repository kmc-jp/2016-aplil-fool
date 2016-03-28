#! /usr/bin/env ruby
begin
  request = $stdin.readline
  method, uri, version = request.split(" ")
  case uri
  when "/"
    puts <<EOS
HTTP/1.0 200 OK
Content-type: image/png

EOS
    print File.read("index.png")
  else
    puts "HTTP/1.0 404 Not Found\n\nNot Found"
  end
rescue => e
  puts "HTTP/1.0 400 Bad Request"
end
