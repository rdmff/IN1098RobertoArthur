import flwr as fl

if __name__ == "__main__":
    # Inicia o servidor FL
    fl.server.start_server(server_address="localhost:8080")
