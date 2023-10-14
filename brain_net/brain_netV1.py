import torch.nn as nn


class BrainNetV1(nn.Module):
    def __init__(self, stage_size, hidden, output, count_layer):
        super(BrainNetV1, self).__init__()
        self.layers = nn.ModuleList([nn.Linear(stage_size, hidden)])
        for _ in range(count_layer - 1):
            self.layers.append(nn.Linear(hidden, hidden))
        self.layers.append(nn.Linear(hidden, output))
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=0.2)
            if module.bias is not None:
                module.bias.data.zero_()

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = nn.functional.relu(layer(x))
        return self.layers[-1](x)
