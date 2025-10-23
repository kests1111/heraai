import torch

def act(x):
    return 0 if x < 0 else 1


def go(arg1, arg2, arg3):
    X = torch.tensor([arg1, arg2, arg3], dtype=torch.float32)
    Wh = torch.tensor([[0.3, 0.3, 0], [0.4, -0.5, 1]])
    Wout = torch.tensor([-1.0, 1.0])


    Zh = torch.mv(Wh, X)
    print(f"Neirosum = {Zh}")


    Uh = torch.tensor([act(x) for x in Zh], dtype=torch.float32)
    print(f"hidden layer neurons = {Uh}")

    Zout = torch.dot(Wout, Uh)
    Y = act(Zout)
    print(f"output value of all that stuff = {Y}")

    return Y

result = go(1, 1 ,1)
print(result)
