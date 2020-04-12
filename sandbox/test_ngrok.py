from pyngrok import ngrok


ngrok.connect(3000)
tunnels = ngrok.get_tunnels()
print(tunnels)

input("enter>")

