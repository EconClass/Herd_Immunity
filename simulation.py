import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.population = []
        self.total_infected = 0
        self.current_infected = 0
        self.next_person_id = 0
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        self.logger = Logger(self.file_name)
        self.vacc_percentage = vacc_percentage
        self.dead = 0
        self.initial_infected = initial_infected
        self.newly_infected = []
    def _create_population(self, initial_infected):
        infected_count = 0
        while len(self.population) < self.population_size:
            if infected_count <  initial_infected:
                infected_person = Person(self.next_person_id, False, self.virus)
                self.population.append(infected_person)
                infected_count += 1
            elif random.random() < self.vacc_percentage:
                self.population.append(Person(self.next_person_id, True, None))

            else:
                self.population.append(Person(self.next_person_id, False, None))
            self.next_person_id += 1
           
        

    def _simulation_should_continue(self):
        self.dead = 0               # resets the value to avoid early termination
        self.current_infected = 0

        for person in self.population:
            if person.is_alive == False:
                self.dead += 1
        for person in self.population: 
            if person.infected and person.is_alive:
                self.current_infected += 1
        if self.dead == len(self.population):
            return False
        elif self.current_infected == 0:
            return False
        else:
            return True


    def run(self):
        time_step_counter = 0
        self._create_population(self.initial_infected)
        should_continue = self._simulation_should_continue()
        while should_continue:
            self.time_step()
            for person in self.population:
                self.logger.log_infection_survival(person, person.did_survive_infection())
            
            self._infect_newly_infected()

            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()
            time_step_counter += 1
        
        for person in self.population:
            if person.infected is not None:
                self.total_infected += 1
        print('The simulation has ended after {} turns.'.format(time_step_counter - 1))

    def time_step(self):
        interactions = 1
        for person in self.population:
            if person.is_alive == True:
                while interactions <= 100:
                    random_interation = random.choice(self.population)
                    while random_interation.is_alive is False or random_interation._id == person._id:
                        random_interation = random.choice(self.population)
                    self.interaction(person, random_interation)
                    interactions += 1


    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True
        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person, False, True, False)
        elif random_person.infected is not None:
            self.logger.log_interaction(person, random_person, False, False, True)
        elif random_person.infected == None and random_person.is_vaccinated == False:
            if random.random() < self.basic_repro_num:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, True, False, False)
        else:
            self.logger.log_interaction(person, random_person, False, False, False)
        

    def _infect_newly_infected(self):
        for num in self.newly_infected:
            for person in self.population:
                if person._id == num:
                    person.infected = self.virus
        self.newly_infected = []
        

Tuberculosis = Simulation(1000, 0.8, "Tuberculosis", 0.65, 0.5, 10)
Tuberculosis.run()
# if __name__ == "__main__":
#     params = sys.argv[0:]
#     print(params)
#     pop_size = int(params[0])
#     vacc_percentage = float(params[1])
#     virus_name = str(params[2])
#     mortality_rate = float(params[3])
#     basic_repro_num = float(params[4])
#     if len(params) == 6:
#         initial_infected = int(params[5])
#     else:
#         initial_infected = 1
#     simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
#                             basic_repro_num, initial_infected)
#     simulation.run()
