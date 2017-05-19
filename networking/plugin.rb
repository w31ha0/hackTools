class Example < BetterCap::Proxy::TCP::Module

  # client -> upstream serve

  def on_data( event )

    BetterCap::Logger.raw "\n#{BetterCap::StreamLogger.hexdump( event.data, :padding => '    ' )}\n"

  end

  # upstream server -> client

  def on_response( event )

    BetterCap::Logger.raw "\n#{BetterCap::StreamLogger.hexdump( event.data, :padding => '    ' )}\n"

  end

end
