docker run --gpus all -p 12001:12001 -v $(pwd):/vits vits bash -c 'python -m uvicorn main:app --host 0.0.0.0 --port 12001'