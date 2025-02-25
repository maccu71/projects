import torch
import time

size = 10000  # Duża macierz 10,000 x 10,000

# CPU Test
A_cpu = torch.rand((size, size))  # Na CPU
B_cpu = torch.rand((size, size))

start = time.time()
C_cpu = torch.mm(A_cpu, B_cpu)  # Mnożenie macierzy na CPU
end = time.time()
print(f"CPU Time: {end - start:.4f} s")

# GPU Test (CUDA)
device = torch.device("cuda")  # Ustawienie GPU
A_gpu = A_cpu.to(device)  # Przenosimy macierz na GPU
B_gpu = B_cpu.to(device)

torch.cuda.synchronize()  # Synchronizacja przed startem pomiaru czasu
start = time.time()
C_gpu = torch.mm(A_gpu, B_gpu)  # Mnożenie na GPU
torch.cuda.synchronize()  # Synchronizacja przed pomiarem końca
end = time.time()
print(f"GPU Time: {end - start:.4f} s")

'''
My results:
CPU Time: 2.9528 s
GPU Time: 0.3411 s

So these tiny 3840 CUDA cores seemed to work ~10x faster than CPU in this case. Amazing!
'''