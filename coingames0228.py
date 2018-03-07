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
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameResults = [] # create an empty list where the loss results will be stored
        self._lossprob = 0

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            self._gameResults.append(game.get_result())

        self._sumStat_meanReward = Stat.SummaryStat("The summary statistic of Mean Reward",self._gameRewards)
        self._sumStat_loss_prob = Stat.SummaryStat("The summary statistic of Loss Probability", self._gameResults)

    def get_all_reward(self):
        return self._gameRewards

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_t_95CI_meanreward(self, alpha_m):
        return self._sumStat_meanReward.get_t_CI(alpha_m)

    def get_all_results(self):
        return self._gameResults

    def prob_lose(self):
        tlr = 0 # the times that you lose money
        for everyreward in self._gameRewards:
            if everyreward < 0:
                tlr += 1
        self._lossprob = tlr/len(self._gameRewards)

        return tlr/len(self._gameRewards)

    def get_t_95CI_lossprob(self,alpha_l):
        return self._sumStat_loss_prob.get_t_CI(alpha_l)

    def get_casino(self,alpha_c):
        self._casino_mean = self._sumStat_meanReward.get_mean()
        self._casino_CI= self._sumStat_meanReward.get_t_CI(alpha_c)
        return self._casino_mean, self._casino_CI

    def get_gambler(self,alpha_g):
        self._gambler_mean = self._sumStat_meanReward.get_mean()
        self._gambler_PI = self._sumStat_meanReward.get_PI(alpha_g)
        return self._gambler_mean, self._gambler_PI

class mutliCohort():
    def __init__(self,ids, popsizes,prob_heads):
        self._ids=ids
        self._popsizes = popsizes
        self._prob_heads = prob_heads

        self._mutli_rewards=[]
        self._meanrewards=[]



#Homework 4
print("Question 4")
# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)

#Homework 6
print("Question 6")
#problem 1
ALPHA_M=0.05
ALPHA_L=0.05
ALPHA_C=0.05
ALPHA_G=0.05
print("problem 1")
print("The 95% CI for expected rewards:",games.get_t_95CI_meanreward(ALPHA_M))
print("The 95% CI for loss probability:", games.get_t_95CI_lossprob(ALPHA_L))

#Problem 2
print("problem 2")
print("The confidence interval for expected reward is [- 31.79, -20.00], which means that if we play the games for 1000 times  "
      "and get a interval for each game, 95% of theses will cover the true mean.")
print("The confidence interval for loss probabilityis [0.58, 0.64], which means that if we play the games for 1000 times and get"
      "intervals for each game, 95% of these intervals will cover the true lossing peobability.")
#Problem 3
print("problem 3")
print("the expected reward and 95% CI for casino owners:",games.get_casino(ALPHA_C))
print("Since casino owners play lots of times, therefore we shall use confidence interval."
      "We are 95% confident that the the average rewards for casino owners will fall in [-31.79, -20.00]")
print("the expected reward and 95% PI for gamblers:",games.get_gambler(ALPHA_G))
print("Since gamblers only play limited times, therefore we shall use projection interval."
      "We are 95% confident that the the average rewards for gamblers will fall in [-152.5, 150]")