import numpy as np
import scr.FigureSupport as Fig
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin
        self._reward = 0
        self._result = 0

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        self._reward = 100*self._countWins - 250
        return self._reward

    def get_result(self):
        if self._reward < 0:
            self._result = 1
        return  self._result



class SetOfGames:
    def __init__(self,id,prob_head, n_games):
        self._id = id
        self._gamelists= []
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameResults = [] # create an empty list where the loss results will be stored
        self._sumStat_Reward = None
        self._sumStat_loss_prob = None
        self._lossprob = 0

        n = 1
        while n <= n_games:
            game = Game(n, prob_head=0.5)# create games
            self._gamelists.append(game)
            n+=1


    def simulate(self,  n_of_flips):
        # simulate the games
        for game in self._gamelists:
            game.simulate(n_of_flips)
            value1 = game.get_reward()
            value2 = game.get_result()
            # store the reward
            self._gameRewards.append(value1)
            self._gameResults.append(value2)

        self._sumStat_Reward = Stat.SummaryStat("The summary statistic of Reward",self._gameRewards)
        self._sumStat_loss_prob = Stat.SummaryStat("The summary statistic of Loss Probability", self._gameResults)

    def get_all_reward(self):
        return self._gameRewards

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_t_95CI_reward(self):
        alpha_m = 0.05
        return self._sumStat_Reward.get_t_CI(alpha_m)

    def get_all_results(self):
        return self._gameResults

    def prob_lose(self):
        tlr = 0 # the times that you lose money
        for everyreward in self._gameRewards:
            if everyreward < 0:
                tlr += 1
        self._lossprob = tlr/len(self._gameRewards)

        return tlr/len(self._gameRewards)

    def get_t_95CI_lossprob(self):
        alpha_l = 0.05
        return self._sumStat_loss_prob.get_t_CI(alpha_l)

class mutliCohort():
    def __init__(self,ids,prob_heads, n_cohorts):
        self._ids=ids
        self._n_cohorts = n_cohorts
        self._prob_heads = prob_heads

        self._mutli_rewards=[]
        self._meanrewards=[]
        self._sumStat_meanrewards = None

    def simulate(self,n_of_flips):
        for i in range (len(self._ids)):
            cohort = SetOfGames(self._ids[i], self._n_cohorts[i], self._prob_heads[i])
            cohort.simulate(n_of_flips)
            self._mutli_rewards.append(cohort.get_all_reward())
            self._meanrewards.append(cohort.get_ave_reward())
            self._sumStat_meanrewards = Stat.SummaryStat("The summary statistic of Mean Reward", self._meanrewards)

    def get_overal_mean_survival(self):
        return self._sumStat_meanrewards.get_mean()

    def get_PI_mean_survival(self,alpha):
        return self._sumStat_meanrewards.get_PI(alpha)

    def get_all_mean_survival(self):
        return self._meanrewards


#Homework 6
print("Homework 6")
PROBHEAD = 0.5
N_GAMES = 1000
#problem 1
print("problem 1")
games = SetOfGames(id = 0, prob_head=PROBHEAD, n_games=N_GAMES)
games.simulate(n_of_flips=20)
print("The 95% CI for expected rewards:",games.get_t_95CI_reward())
print("The 95% CI for loss probability:", games.get_t_95CI_lossprob())

#Problem 2
print("problem 2")
print("The confidence interval for expected reward is [- 28.56, -16.24], which means that if we play the games for 1000 times  "
      "and get a interval for each game, 95% of theses will cover the true mean.")
print("The confidence interval for loss probabilityis [0.55, 0.62], which means that if we play the games for 1000 times and get"
      "intervals for each game, 95% of these intervals will cover the true lossing peobability.")
#Problem 3
print("problem 3")
print("the expected reward for casino owners is:", games.get_t_95CI_reward(),
      "and 95% CI for casino owners:",games.get_ave_reward())
print("Since casino owners play lots of times, therefore we shall use confidence interval."
      "We are 95% confident that the the average rewards for casino owners will fall in [- 28.56, -16.24]")

print("fot gamblers")
gambler = mutliCohort(ids=range(1000),
                      prob_heads=[0.5]*1000,
                      n_cohorts=[10]*1000)
gambler.simulate(20)
print("the expected reward and 95% PI for gamblers:",gambler.get_PI_mean_survival())
print("Since gamblers only play limited times, therefore we shall use projection interval."
      "We are 95% confident that the the average rewards for gamblers will fall in [-152.5, 150]")
