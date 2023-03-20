import os.path
import numpy as np
from plotting.base import plt, colors

beliefColor = colors['pomdp']

def traj(experiment_name, Sessions, outdir, hidden_size, xline, input_name, xmax=200):
    # Figs 5C, S2A: plot distance from ITI following observations, across models
    plt.figure(figsize=(2.5,2.5))
    rnns = Sessions[('value-rnn-trained', hidden_size)]
    keyname = input_name if input_name == 'odor' else 'rew'
    for i, rnn in enumerate(rnns):
        ds = rnn['results']['memories']['{}_memories'.format(keyname)][0]['distances']
        plt.plot(ds/ds.max(), alpha=0.8)
    plt.xlabel('Time steps rel.\nto {} input'.format(input_name), fontsize=12)
    plt.ylabel('Rel. distance from ITI', fontsize=12)
    plt.plot(xline*np.ones(2), [0, 1], '--', color=beliefColor)
    plt.ylim([0, 1.01])
    plt.xlim([0,xmax])
    plt.yticks([0, 0.5, 1])
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, '{}_{}-memory_trajs.pdf'.format(experiment_name, input_name)))
    plt.close()

def histogram(experiment_name, Sessions, outdir, hidden_size, xline, input_name, xmax=200):
    # Figs 5D, S2B: plot histogram of odor/reward memories
    plt.figure(figsize=(2.5,2.5))
    bins = np.linspace(0, xmax, 20)

    rnns = Sessions[('value-rnn-trained', hidden_size)]
    keyname = input_name if input_name == 'odor' else 'rew'
    vs = [rnn['results']['memories']['{}_memories'.format(keyname)][0]['duration'] for rnn in rnns]

    ys, xs = np.histogram(vs, bins=bins)
    print('{} ({}, {}: {:0.2f} ± {:0.2f})'.format(experiment_name, input_name, np.median(vs), np.mean(vs), np.std(vs)/np.sqrt(len(vs))))

    xs = [np.mean([xs[i], xs[i+1]]) for i in range(len(xs)-1)]
    width = np.diff(xs[:-1]).mean()
    plt.bar(xs, 100*ys/len(vs), width=width)
    plt.bar(xmax-width/2, len(vs)-ys.sum(), width=width, alpha=0.5)
    plt.plot(xline*np.ones(2), [0, 100], '--', color=beliefColor)
    
    plt.xlabel('Memory duration')
    plt.ylabel('% of RNNs')
    plt.xlim([-np.diff(xs).mean(), xmax])
    plt.ylim([0, 100])
    plt.yticks(np.arange(0,101,25))
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, '{}_{}-memory_hists.pdf'.format(experiment_name, input_name)))
    plt.close()
