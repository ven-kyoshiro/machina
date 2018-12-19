# Copyright 2018 DeepX Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import numpy as np
import torch
from torch.distributions import Normal, kl_divergence

from machina.pds.base import BasePd


class GaussianPd(BasePd):
    def __init__(self, ob_space, ac_space):
        BasePd.__init__(self, ob_space, ac_space)

    def sample(self, params, sample_shape=torch.Size()):
        mean, log_std = params['mean'], params['log_std']
        std = torch.exp(log_std)
        ac = Normal(loc=mean, scale=std).rsample(sample_shape)
        return ac

    def llh(self, x, params):
        mean, log_std = params['mean'], params['log_std']
        std = torch.exp(log_std)
        return Normal(loc=mean, scale=std).log_prob(x)

    def kl_pq(self, p_params, q_params):
        p_mean, p_log_std = p_params['mean'], p_params['log_std']
        q_mean, q_log_std = q_params['mean'], q_params['log_std']
        p_std = torch.exp(p_log_std)
        q_std = torch.exp(q_log_std)
        return kl_divergence(Normal(loc=p_mean, scale=p_std), Normal(loc=q_mean, scale=q_std))

    def ent(self, params):
        mean = params['mean']
        log_std = params['log_std']
        std = torch.exp(log_std)
        return Normal(loc=mean, scale=std).entropy()
