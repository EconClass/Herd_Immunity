import logging

class Logger(object):
    def __init__(self, file_name):
        self.file_name = str(file_name)

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        new_line = open(self.file_name, "w")
        inputs = "PARAMETERS \t Population: {} \t Vaccinated: {} \t Virus: {} \t Mortality Rate: {} \t Reproduction: {} \n".format(str(pop_size), str(vacc_percentage), virus_name, str(mortality_rate), str(basic_repro_num))
        new_line.write(inputs)

    def log_interaction(self, person1, person2, did_infect=None, person2_vacc=None, person2_sick=None):
        add_lines = open(self.file_name, "a")
        if did_infect == True:
            add_lines.write("Citizen {} has infected {}! \n ".format(person1._id, person2._id))
        elif person2_vacc == True:
            add_lines.write("Citizen {} has been immunized against the virus! \n".format(person2._id))
        elif person2_sick == True:
            add_lines.write("Citizen {} has already been infected! \n".format(person2._id))
        else:
            add_lines.write("Citizen {}is naturally immune to the virus! \n".format(person2._id))

    def log_infection_survival(self, person, did_die_from_infection):
        add_lines = open(self.file_name, "a")
        if did_die_from_infection:      # Use the result form the did_survive_infection() 
            did_die_from_infection = False
            add_lines.write("Citizen {} has survived the infection! \n".format(person._id))
        else:
            add_lines.write("R.I.P. Citizen {}! \n".format(person._id))

    def log_time_step(self, time_step_number):
        add_lines = open(self.file_name, "a")
        add_lines.write("End of time step: {} \n".format(time_step_number))