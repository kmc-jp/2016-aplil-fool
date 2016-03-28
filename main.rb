#! /usr/bin/env ruby
begin
  request = $stdin.readline
  method, uri, version = request.split(" ")
  case uri
  when "/"
    puts <<EOS
HTTP/1.0 200 OK

<!doctype html>
<p>work</p>
EOS
  else
    puts "HTTP/1.0 404 Not Found"
  end
rescue => e
  puts "HTTP/1.0 400 Bad Request"
end
