from .app_factory import create_app, AlgorithmApp
import argparse


def run_service(algorithms: list, service_port: int = 5000, backend_url: str = None):
    parser = argparse.ArgumentParser(description='Algorithm Service')
    parser.add_argument('--port', type=int, default=service_port,
                        help='Service port')
    parser.add_argument('--backend', type=str, default=backend_url,
                        help='Backend URL for registration')
    args = parser.parse_args()

    app = create_app(algorithms, args.port, args.backend)
    print(f"Starting algorithm service on port {args.port}...")
    app.run()