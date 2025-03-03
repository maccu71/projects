import torch
import time

size = 10000  # Large matrix 10,000 x 10,000

# CPU Test
A_cpu = torch.rand((size, size))  # On CPU
B_cpu = torch.rand((size, size))

start = time.time()
C_cpu = torch.mm(A_cpu, B_cpu)  # multiplication macierzy na CPU
end = time.time()
print(f"CPU Time: {end - start:.4f} s")

# GPU Test (CUDA)
device = torch.device("cuda")  # GPU settings
A_gpu = A_cpu.to(device)  # Send matrix to GPU
B_gpu = B_cpu.to(device)

torch.cuda.synchronize()  # Sync before star of the measurement 
start = time.time()
C_gpu = torch.mm(A_gpu, B_gpu)  # Multiplication on GPU
torch.cuda.synchronize()  # Sync before end of the measurement 
end = time.time()
print(f"GPU Time: {end - start:.4f} s")

'''
My results:
CPU Time: 2.9528 s
GPU Time: 0.3411 s

So these tiny (who know how many were forced to labour?) 
CUDA cores seemed to work ~10x faster than CPU alone in this case..
Amazing!
'''