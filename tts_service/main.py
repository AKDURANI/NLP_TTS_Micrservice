import grpc
from concurrent import futures

import sys
import os


# Add grpc_gen to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'grpc_gen')))

import app.core as core
import tts_pb2
import tts_pb2_grpc


# Define the TTS Service
class TTSService(tts_pb2_grpc.TextToSpeechServicer):
    def GenerateAudio(self, request, context):
        try:
            # Run core logic
            path = core.generate_audio(
                pdf_path=request.pdf_path,
                page_range=(request.start_page, request.end_page)
            )
            return tts_pb2.GenerateReply(
                output_audio_path=path,
                message="Success"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return tts_pb2.GenerateReply(
                output_audio_path="",
                message=f"Error occurred: {str(e)}"
            )

# Create the gRPC server with increased concurrency
def serve():
    # Create the gRPC server with a ThreadPoolExecutor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add our service to the server
    tts_pb2_grpc.add_TextToSpeechServicer_to_server(TTSService(), server)
    
    # Open the port on localhost:50051
    server.add_insecure_port('[::]:50051')
    
    # Start the server
    print("✅ gRPC server running at http://localhost:50051")
    server.start()
    
    # Keep the server running indefinitely
    server.wait_for_termination()

# Run the server
if __name__ == "__main__":
    serve()
