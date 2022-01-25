import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import scipy


def make_decision(p_value, alpha):
    if p_value <= alpha:
        decision = f"P-value is lower than {alpha}. Null hypothesis has been rejected!"
    else:
        decision = f"P-value is higher than {alpha}. There is not enough evidence to reject the null hypothesis!"
    return decision


def two_sample_t_test(first_sample_mean, first_sample_std, second_sample_mean, second_sample_std, first_N, second_N, alpha=0.05, type="two-sided"):
  
    test_stat = round((first_sample_mean - second_sample_mean) / ((first_sample_std**2/first_N) + (second_sample_std**2/second_N ))**(1/2),2)
    dof = round(first_N + second_N - 2,0)
    ub = 1.96
    lb = -1.96


    if type == "two-sided":
        lb = scipy.stats.t.ppf(alpha/2, dof)
        ub = -scipy.stats.t.ppf(alpha/2, dof)
        p_value = round(2 - 2 * scipy.stats.t.cdf(abs(test_stat), dof),3)
        
    elif type == "left-sided":
        lb = scipy.stats.t.ppf(alpha, dof)
        p_value = round(scipy.stats.t.cdf(test_stat, dof),3)

    elif type == "right-sided":
        ub = - scipy.stats.t.ppf(alpha, dof)
        p_value = round(1 - scipy.stats.t.cdf(test_stat, dof),3)

    decision = make_decision(p_value, alpha)

    return {"test_stat":test_stat, "p-value":p_value, "lb":lb, "ub":ub, "degrees_of_freedom":dof, "type":type, "decision":decision, "alpha":alpha}


def plot_t_student(df=1000, lb=None, ub=None, type="two-sided", stat_value=0):
    x = np.linspace(scipy.stats.t.ppf(0.01, df), scipy.stats.t.ppf(0.99, df), 1000)
    
    plt.plot(x, scipy.stats.t.pdf(x, df), color = 'blue')


    if type == "two-sided":
        px_lower = np.arange(min(x), lb, 0.01)
        plt.fill_between(px_lower, scipy.stats.t.pdf(px_lower, df), color='red')

        px_upper = np.arange(ub, max(x), 0.01)
        plt.fill_between(px_upper, scipy.stats.t.pdf(px_upper, df), color='red')
    elif type == "left-sided":
        px_lower = np.arange(min(x), lb, 0.01)
        plt.fill_between(px_lower, scipy.stats.t.pdf(px_lower, df), color="red")
    elif type == "right-sided":
        px_upper = np.arange(ub, max(x), 0.01)
        plt.fill_between(px_upper, scipy.stats.t.pdf(px_upper, df), color="red")

    plt.axvline(x=stat_value, color="green")
    plt.savefig('/static/ttestimg.img')
