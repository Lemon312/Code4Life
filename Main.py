import sys
import math


# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
class Module:
    EMPTY = ''
    START_POS = 'START_POS'
    SAMPLES = 'SAMPLES'
    DIAGNOSIS = 'DIAGNOSIS'
    MOLECULES = 'MOLECULES'
    LABORATORY = 'LABORATORY'


class Storage:
    MAX_TOTAL_STORAGE_NUM = 10
    MAX_SINGEL_STORAGE_NUM = 5

    def __init__(self):
        self.storage_a = 0
        self.storage_b = 0
        self.storage_c = 0
        self.storage_d = 0
        self.storage_e = 0

    def get_used_storage(self):
        return self.storage_a + self.storage_b + self.storage_c + self.storage_d + self.storage_e

    def get_unused_storage(self):
        return self.MAX_TOTAL_STORAGE_NUM - (
                self.storage_a + self.storage_b + self.storage_c + self.storage_d + self.storage_e)

    def is_full(self):
        return self.get_used_storage() == self.MAX_TOTAL_STORAGE_NUM

    def is_empty(self):
        return self.get_used_storage() == 0

    def get_minimum_storage(self):
        minimum_storage = self.storage_a

        if minimum_storage == 0 \
                or self.storage_b < minimum_storage:
            minimum_storage = self.storage_b
        if minimum_storage == 0 \
                or self.storage_c < minimum_storage:
            minimum_storage = self.storage_c
        if minimum_storage == 0 \
                or self.storage_d < minimum_storage:
            minimum_storage = self.storage_d
        if minimum_storage == 0 \
                or self.storage_e < minimum_storage:
            minimum_storage = self.storage_e
        return minimum_storage

    def get_maximum_storage(self):
        maximum_storage = self.storage_a
        if maximum_storage == 0 \
                or self.storage_b > maximum_storage:
            maximum_storage = self.storage_b
        if maximum_storage == 0 \
                or self.storage_c > maximum_storage:
            maximum_storage = self.storage_c
        if maximum_storage == 0 \
                or self.storage_d > maximum_storage:
            maximum_storage = self.storage_d
        if maximum_storage == 0 \
                or self.storage_e > maximum_storage:
            maximum_storage = self.storage_e
        return maximum_storage

    def debug_print(self, pre_fix):
        print("DEBUG: ", pre_fix,
              "storage.storage_a=", self.storage_a,
              "storage.storage_b=", self.storage_b,
              "storage.storage_c=", self.storage_c,
              "storage.storage_d=", self.storage_d,
              "storage.storage_e=", self.storage_e,
              file=sys.stderr)


class Expertise:
    def __init__(self):
        self.expertise_a = 0
        self.expertise_b = 0
        self.expertise_c = 0
        self.expertise_d = 0
        self.expertise_e = 0

    def get_total_expertise(self):
        return self.expertise_a + self.expertise_b + self.expertise_c + self.expertise_d + self.expertise_e


class ScienceProject:
    def __init__(self, project_id, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e):
        self.project_id = project_id
        self.expertise = Expertise()
        self.expertise.expertise_a = expertise_a
        self.expertise.expertise_b = expertise_b
        self.expertise.expertise_c = expertise_c
        self.expertise.expertise_d = expertise_d
        self.expertise.expertise_e = expertise_e
        self.total_expertise = expertise_a + expertise_b + expertise_c + expertise_d + expertise_e

        print("new a science project, project_id", self.project_id,
              ",expertise_a", self.expertise.expertise_a,
              ",expertise_b", self.expertise.expertise_b, ",expertise_c", self.expertise.expertise_c, ",expertise_d ",
              self.expertise.expertise_d,
              ",expertise_e ", self.expertise.expertise_e, ",total_expertise ", self.total_expertise, file=sys.stderr)


class Sample:
    def __init__(self, game, sample_id, carried_by, health, rank, expertise_gain, total_cost, cost_a, cost_b, cost_c,
                 cost_d, cost_e):
        self.game = game
        self.sample_id = sample_id
        self.carried_by = carried_by
        self.health = health
        self.rank = rank
        self.expertise_gain = expertise_gain
        self.total_cost = total_cost
        self.cost_a = cost_a
        self.cost_b = cost_b
        self.cost_c = cost_c
        self.cost_d = cost_d
        self.cost_e = cost_e

        self.deleted_flag = False
        self.uploaded_flag = False

    def update_sample(self, sample):
        self.carried_by = sample.carried_by
        self.health = sample.health
        self.rank = sample.rank
        self.expertise_gain = sample.expertise_gain
        self.total_cost = sample.total_cost
        self.cost_a = sample.cost_a
        self.cost_b = sample.cost_b
        self.cost_c = sample.cost_c
        self.cost_d = sample.cost_d
        self.cost_e = sample.cost_e

    def mark_sample_to_be_uploaded(self):
        self.uploaded_flag = True

    def mark_sample_to_be_deleted(self):
        self.deleted_flag = True

    def has_been_marked_as_deleted(self):
        return self.deleted_flag

    def has_been_diagnosed(self):
        if self.health <= 0:
            return False
        else:
            return True

    def get_gain_expertise(self):
        gain_expertise = Expertise()

        if self.expertise_gain == 'A':
            gain_expertise.expertise_a = 1
        elif self.expertise_gain == 'B':
            gain_expertise.expertise_b = 1
        elif self.expertise_gain == 'C':
            gain_expertise.expertise_c = 1
        elif self.expertise_gain == 'D':
            gain_expertise.expertise_d = 1
        elif self.expertise_gain == 'E':
            gain_expertise.expertise_e = 1

        return gain_expertise

    def should_be_uploaded(self, robot):
        if self.has_been_diagnosed() is False:
            print("please diagnose sample id",
                  self.sample_id,
                  "before checking it should be uploaded or not", file=sys.stderr)
            return False
        else:
            needed_storage = robot.get_sample_needed_storage(self)

            if needed_storage.get_used_storage() > Storage.MAX_TOTAL_STORAGE_NUM \
                    or needed_storage.storage_a > self.game.get_max_molecuse_a() \
                    or needed_storage.storage_b > self.game.get_max_molecuse_b() \
                    or needed_storage.storage_c > self.game.get_max_molecuse_c() \
                    or needed_storage.storage_d > self.game.get_max_molecuse_d() \
                    or needed_storage.storage_e > self.game.get_max_molecuse_e():
                return True

        return False


class SampleList:
    MAX_CARRIED_SAMPLE_NUM = 3

    def __init__(self):
        self.sample_list = []

    def add_sample(self, sample):
        for i in range(len(self.sample_list)):
            if sample.sample_id == self.sample_list[i].sample_id:
                self.sample_list.remove(self.sample_list[i])
                break

        for i in range(len(self.sample_list)):
            if sample.total_cost < self.sample_list[i].total_cost:
                self.sample_list.insert(i, sample)
                return
            elif sample.total_cost == self.sample_list[i].total_cost:
                if sample.health > self.sample_list[i].health:
                    self.sample_list.insert(i, sample)
                    return

        self.sample_list.append(sample)

    def delete_all_sample(self):
        self.sample_list = []

    def is_full(self):
        return len(self.sample_list) == self.MAX_CARRIED_SAMPLE_NUM

    def is_empty(self):
        return len(self.sample_list) == 0

    def size(self):
        return len(self.sample_list)

    def get_sample_by_index(self, index):
        if index > len(self.sample_list) - 1:
            return None
        else:
            return self.sample_list[index]

    def get_sample_by_id(self, sample_id):
        for i in range(len(self.sample_list)):
            if sample_id == self.sample_list[i].sample_id:
                return self.sample_list[i]

        return None

    def mark_sample_need_to_be_deleted(self, sample_id):
        for i in range(len(self.sample_list)):
            if sample_id == self.sample_list[i].sample_id:
                self.sample_list[i].mark_sample_to_be_deleted()
                print("sample id", sample_id, " mark as need to be deleted", file=sys.stderr)
                return

    def get_undiagnosed_sample_id(self):
        for i in range(len(self.sample_list)):
            if self.sample_list[i].has_been_diagnosed() is False:
                print("find an undiagnosed sample id", self.sample_list[i].sample_id, " in carrying sample",
                      file=sys.stderr)
                return self.sample_list[i].sample_id

        return -1

    def is_undiagnosed(self, sample_id):
        for i in range(len(self.sample_list)):
            if self.sample_list[i].sample_id == sample_id \
                    and self.sample_list[i].has_been_diagnosed():
                print("sample id", self.sample_list[i].sample_id, "is undiagnosed in carrying sample",
                      file=sys.stderr)
                return True

        return False

    def get_single_molecuse_sample(self):
        for i in range(len(self.sample_list)):
            if self.sample_list[i].total_cost == self.sample_list[i].cost_a:
                return self.sample_list[i]
            if self.sample_list[i].total_cost == self.sample_list[i].cost_b:
                return self.sample_list[i]
            if self.sample_list[i].total_cost == self.sample_list[i].cost_c:
                return self.sample_list[i]
            if self.sample_list[i].total_cost == self.sample_list[i].cost_d:
                return self.sample_list[i]
            if self.sample_list[i].total_cost == self.sample_list[i].cost_e:
                return self.sample_list[i]
        return None

    def get_being_uploaded_sample_id(self, human_robot, ai_robot):
        for i in range(len(self.sample_list)):
            if self.sample_list[i].should_be_uploaded(human_robot):
                print("find an being uploaded sample id", self.sample_list[i].sample_id,
                      " in carrying sample", file=sys.stderr)
                return self.sample_list[i].sample_id

            # human_needed_storage = human_robot.get_sample_needed_storage(self.sample_list[i])
            # if self.sample_list[i].game.get_available_molecuse_a() == 0 \
            #         and human_needed_storage.storage_a > 0 \
            #         and ai_robot.may_spend_storage('A', human_needed_storage.storage_a) is False:
            #     return self.sample_list[i].sample_id
            # if self.sample_list[i].game.get_available_molecuse_b() == 0 \
            #         and human_needed_storage.storage_b > 0 \
            #         and ai_robot.may_spend_storage('B', human_needed_storage.storage_b) is False:
            #     return self.sample_list[i].sample_id
            # if self.sample_list[i].game.get_available_molecuse_c() == 0 \
            #         and human_needed_storage.storage_c > 0 \
            #         and ai_robot.may_spend_storage('C', human_needed_storage.storage_c) is False:
            #     return self.sample_list[i].sample_id
            # if self.sample_list[i].game.get_available_molecuse_d() == 0 \
            #         and human_needed_storage.storage_d > 0 \
            #         and ai_robot.may_spend_storage('D', human_needed_storage.storage_d) is False:
            #     return self.sample_list[i].sample_id
            # if self.sample_list[i].game.get_available_molecuse_e() == 0 \
            #         and human_needed_storage.storage_e > 0 \
            #         and ai_robot.may_spend_storage('E', human_needed_storage.storage_e) is False:
            #     return self.sample_list[i].sample_id

        return -1


class Robot:
    TYPE_AI = 'AI_ROBOT'
    TYPE_HUMAN = 'HUMAN_ROBOT'

    def __init__(self, game, robot_type):
        self.game = game
        self.robot_type = robot_type
        self.previous_target = ''
        self.current_target = Module.START_POS
        self.carrying_sample = SampleList()
        self.enough_molecuses_sample_id_list = []

        self.eta = 0
        self.score = 0
        self.pre_storage = Storage()
        self.storage = Storage()
        self.expertise = Expertise()

    def set_previous_target(self, previous_target):
        self.previous_target = previous_target

    def set_current_target(self, target):
        self.current_target = target

    def set_eta(self, eta):
        self.eta = eta

    def set_score(self, score):
        self.score = score

    def prepare(self):
        self.enough_molecuses_sample_id_list = []
        for i in range(self.carrying_sample.size()):
            if self.has_sample_got_enough_molecuse(self.carrying_sample.get_sample_by_index(i)):
                self.add_sample_id_to_enough_molecuse_sample_list(
                    self.carrying_sample.get_sample_by_index(i).sample_id)

    def clean_up(self):
        self.set_previous_target(self.current_target)

        max_range = self.carrying_sample.size()
        i = 0
        while i < self.carrying_sample.size():
            if self.carrying_sample.get_sample_by_index(i).has_been_marked_as_deleted():
                self.delete_sample_id_from_enough_molecuse_sample_list(
                    self.carrying_sample.get_sample_by_index(i).sample_id)

            i = i + 1

        self.carrying_sample.delete_all_sample()

    def get_consumed_storage(self):
        consumed_storage = Storage()

        total_gain_expertise = Expertise()

        for i in range(len(self.enough_molecuses_sample_id_list)):
            sample = self.carrying_sample.get_sample_by_id(self.enough_molecuses_sample_id_list[i])
            if sample.cost_a > self.expertise.expertise_a:
                consumed_storage.storage_a = \
                    sample.cost_a - self.expertise.expertise_a - total_gain_expertise.expertise_a + consumed_storage.storage_a
            if sample.cost_b > self.expertise.expertise_b:
                consumed_storage.storage_b = \
                    sample.cost_b - self.expertise.expertise_b - total_gain_expertise.expertise_b + consumed_storage.storage_b
            if sample.cost_c > self.expertise.expertise_c:
                consumed_storage.storage_c = \
                    sample.cost_c - self.expertise.expertise_c - total_gain_expertise.expertise_c + consumed_storage.storage_c
            if sample.cost_d > self.expertise.expertise_d:
                consumed_storage.storage_d = \
                    sample.cost_d - self.expertise.expertise_d - total_gain_expertise.expertise_d + consumed_storage.storage_d
            if sample.cost_e > self.expertise.expertise_e:
                consumed_storage.storage_e = \
                    sample.cost_e - self.expertise.expertise_e - total_gain_expertise.expertise_e + consumed_storage.storage_e

            gain_expertise = sample.get_gain_expertise()
            total_gain_expertise.expertise_a = \
                total_gain_expertise.expertise_a + gain_expertise.expertise_a
            total_gain_expertise.expertise_b = \
                total_gain_expertise.expertise_b + gain_expertise.expertise_b
            total_gain_expertise.expertise_c = \
                total_gain_expertise.expertise_c + gain_expertise.expertise_c
            total_gain_expertise.expertise_d = \
                total_gain_expertise.expertise_d + gain_expertise.expertise_d
            total_gain_expertise.expertise_e = \
                total_gain_expertise.expertise_e + gain_expertise.expertise_e

        return consumed_storage

    def get_unconsumed_storage(self):
        unconsumed_storage = Storage()
        consumed_storage = self.get_consumed_storage()
        unconsumed_storage.storage_a = self.storage.storage_a - consumed_storage.storage_a
        unconsumed_storage.storage_b = self.storage.storage_b - consumed_storage.storage_b
        unconsumed_storage.storage_c = self.storage.storage_c - consumed_storage.storage_c
        unconsumed_storage.storage_d = self.storage.storage_d - consumed_storage.storage_d
        unconsumed_storage.storage_e = self.storage.storage_e - consumed_storage.storage_e

        return unconsumed_storage

    def is_in_enough_molecuses_sample_id_list(self, sample_id):
        for i in range(len(self.enough_molecuses_sample_id_list)):
            if sample_id == self.enough_molecuses_sample_id_list[i]:
                return True

        return False

    def add_sample_id_to_enough_molecuse_sample_list(self, sample_id):
        if self.is_in_enough_molecuses_sample_id_list(sample_id) is False:
            self.enough_molecuses_sample_id_list.append(sample_id)
            if self.robot_type == self.TYPE_HUMAN:
                print("DEBUG: " + self.robot_type + " add sample id",
                      sample_id, "to enough molecuse sample list", file=sys.stderr)

    def delete_sample_id_from_enough_molecuse_sample_list(self, sample_id):
        for i in range(len(self.enough_molecuses_sample_id_list)):
            if sample_id == self.enough_molecuses_sample_id_list[i]:
                self.enough_molecuses_sample_id_list.remove(sample_id)
                print("DEBUG: " + self.robot_type + " delete sample id",
                      sample_id, "from enough molecuse sample list", file=sys.stderr)
                return

    def get_enough_molecuses_sample_size(self):
        return len(self.enough_molecuses_sample_id_list)

    def has_sample_got_enough_molecuse(self, sample):
        if sample is None:
            return False

        if sample.has_been_diagnosed() is False \
                or sample.should_be_uploaded(self):
            return False

        needed_storage = self.get_sample_needed_storage(sample)
        if needed_storage.get_used_storage() == 0:
            return True
        else:
            return False

    def get_sample_needed_storage(self, sample):
        needed_storage = Storage()

        if sample is None:
            return needed_storage

        if self.is_in_enough_molecuses_sample_id_list(sample.sample_id):
            return needed_storage
        else:
            unconsumed_storage = self.get_unconsumed_storage()

            if sample.has_been_diagnosed() is False:
                return needed_storage

            if sample.cost_a > (unconsumed_storage.storage_a + self.expertise.expertise_a):
                needed_storage.storage_a = \
                    sample.cost_a - (unconsumed_storage.storage_a + self.expertise.expertise_a)
            if sample.cost_b > (unconsumed_storage.storage_b + self.expertise.expertise_b):
                needed_storage.storage_b = \
                    sample.cost_b - (unconsumed_storage.storage_b + self.expertise.expertise_b)
            if sample.cost_c > (unconsumed_storage.storage_c + self.expertise.expertise_c):
                needed_storage.storage_c = \
                    sample.cost_c - (unconsumed_storage.storage_c + self.expertise.expertise_c)
            if sample.cost_d > (unconsumed_storage.storage_d + self.expertise.expertise_d):
                needed_storage.storage_d = \
                    sample.cost_d - (unconsumed_storage.storage_d + self.expertise.expertise_d)
            if sample.cost_e > (unconsumed_storage.storage_e + self.expertise.expertise_e):
                needed_storage.storage_e = \
                    sample.cost_e - (unconsumed_storage.storage_e + self.expertise.expertise_e)

        return needed_storage

    def get_best_block_storage_in_all_sample(self):
        minimum_needed_storage = Storage()
        storage_count = Storage()

        for i in range(self.carrying_sample.size()):
            sample = self.carrying_sample.get_sample_by_index(i)
            needed_storage = self.get_sample_needed_storage(sample)

            if needed_storage.storage_a > 0:
                storage_count.storage_a = needed_storage.storage_a + 1
                if minimum_needed_storage.storage_a == 0 \
                        or needed_storage.storage_a < minimum_needed_storage.storage_a:
                    minimum_needed_storage.storage_a = needed_storage.storage_a

            if needed_storage.storage_b > 0:
                storage_count.storage_b = needed_storage.storage_b + 1
                if minimum_needed_storage.storage_b == 0 \
                        or needed_storage.storage_b < minimum_needed_storage.storage_b:
                    minimum_needed_storage.storage_b = needed_storage.storage_b

            if needed_storage.storage_c > 0:
                storage_count.storage_c = needed_storage.storage_c + 1
                if minimum_needed_storage.storage_c == 0 \
                        or needed_storage.storage_c < minimum_needed_storage.storage_c:
                    minimum_needed_storage.storage_c = needed_storage.storage_c

            if needed_storage.storage_d > 0:
                storage_count.storage_d = needed_storage.storage_d + 1
                if minimum_needed_storage.storage_d == 0 \
                        or needed_storage.storage_d < minimum_needed_storage.storage_d:
                    minimum_needed_storage.storage_d = needed_storage.storage_d

            if needed_storage.storage_e > 0:
                storage_count.storage_e = needed_storage.storage_e + 1
                if minimum_needed_storage.storage_e == 0 \
                        or needed_storage.storage_e < minimum_needed_storage.storage_e:
                    minimum_needed_storage.storage_e = needed_storage.storage_e

        max_count = storage_count.get_maximum_storage()
        if storage_count.storage_a != max_count:
            minimum_needed_storage.storage_a = 0
        if storage_count.storage_b != max_count:
            minimum_needed_storage.storage_b = 0
        if storage_count.storage_c != max_count:
            minimum_needed_storage.storage_c = 0
        if storage_count.storage_d != max_count:
            minimum_needed_storage.storage_d = 0
        if storage_count.storage_e != max_count:
            minimum_needed_storage.storage_e = 0

        return minimum_needed_storage

    def may_spend_storage(self, storage_type, storage_number):
        if self.current_target != Module.MOLECULES and self.current_target != Module.LABORATORY:
            return True

        for i in range(self.carrying_sample.size()):
            sample = self.carrying_sample.get_sample_by_index(i)
            if storage_type == 'A' \
                    and sample.cost_a > 0 \
                    and self.storage.storage_a > 0 \
                    and (sample.cost_a - self.expertise.expertise_a - self.storage.storage_a > 0):
                return True
            if storage_type == 'B' \
                    and sample.cost_b > 0 \
                    and self.storage.storage_b > 0 \
                    and (sample.cost_b - self.expertise.expertise_b - self.storage.storage_b > 0):
                return True
            if storage_type == 'C' \
                    and sample.cost_c > 0 \
                    and self.storage.storage_c > 0 \
                    and (sample.cost_c - self.expertise.expertise_c - self.storage.storage_c > 0):
                return True
            if storage_type == 'D' \
                    and sample.cost_d > 0 \
                    and self.storage.storage_d > 0 \
                    and (sample.cost_d - self.expertise.expertise_d - self.storage.storage_d > 0):
                return True
            if storage_type == 'E' \
                    and sample.cost_e > 0 \
                    and self.storage.storage_e > 0 \
                    and (sample.cost_e - self.expertise.expertise_e - self.storage.storage_e > 0):
                return True
        return False

    def get_one_enough_molecules_sample_id(self):
        if len(self.enough_molecuses_sample_id_list) > 0:
            return self.enough_molecuses_sample_id_list[0]

        return -1

    def get_sample_id_which_should_fetch_molecuses(self):
        for i in range(self.carrying_sample.size()):
            sample = self.carrying_sample.get_sample_by_index(i)
            if self.has_sample_got_enough_molecuse(sample) is False:
                print("DEBUG: " + self.robot_type + " find sample id",
                      self.carrying_sample.get_sample_by_index(i).sample_id,
                      "should fetch molecuses ", file=sys.stderr)

                return sample.sample_id

        print("DEBUG: " + self.robot_type + " Not found sample should fetch molecuses ", file=sys.stderr)
        return -1


class Game:
    INIT_MAX_MOLECUSE_NUMBER = 5

    def __init__(self):
        self.turn = 0
        self.cloud_sample = SampleList()
        self.scienceProjects = []
        self.enough_molecuses_sample_id_list_for_human_robot = []

        self.human_robot = None
        self.ai_robot = None

        self.additional_mollecuse_a = 0
        self.additional_mollecuse_b = 0
        self.additional_mollecuse_c = 0
        self.additional_mollecuse_d = 0
        self.additional_mollecuse_e = 0

    def set_human_robot(self, human_robot):
        self.human_robot = human_robot

    def set_ai_robot(self, ai_robot):
        self.ai_robot = ai_robot

    def prepare(self):
        self.enough_molecuses_sample_id_list_for_human_robot = []
        for i in range(self.cloud_sample.size()):
            if self.human_robot.has_sample_got_enough_molecuse(self.cloud_sample.get_sample_by_index(i)):
                self.enough_molecuses_sample_id_list_for_human_robot.append(
                    self.cloud_sample.get_sample_by_index(i).sample_id)
                print("GAME find sample id", self.cloud_sample.get_sample_by_index(i).sample_id,
                      "got enough molecuse for human robot", file=sys.stderr)

    def clean_up(self):
        self.turn = self.turn + 1
        print("DEBUG:  game turn =", self.turn, file=sys.stderr)

        self.cloud_sample.delete_all_sample()

    def add_science_project(self, science_project):
        self.scienceProjects.append(science_project)

    def get_max_molecuse_a(self):
        return self.INIT_MAX_MOLECUSE_NUMBER + self.additional_mollecuse_a

    def get_max_molecuse_b(self):
        return self.INIT_MAX_MOLECUSE_NUMBER + self.additional_mollecuse_b

    def get_max_molecuse_c(self):
        return self.INIT_MAX_MOLECUSE_NUMBER + self.additional_mollecuse_c

    def get_max_molecuse_d(self):
        return self.INIT_MAX_MOLECUSE_NUMBER + self.additional_mollecuse_d

    def get_max_molecuse_e(self):
        return self.INIT_MAX_MOLECUSE_NUMBER + self.additional_mollecuse_e

    def get_available_molecuse_a(self):
        return self.get_max_molecuse_a() - self.human_robot.storage.storage_a - self.ai_robot.storage.storage_a

    def get_available_molecuse_b(self):
        return self.get_max_molecuse_b() - self.human_robot.storage.storage_b - self.ai_robot.storage.storage_b

    def get_available_molecuse_c(self):
        return self.get_max_molecuse_c() - self.human_robot.storage.storage_c - self.ai_robot.storage.storage_c

    def get_available_molecuse_d(self):
        return self.get_max_molecuse_d() - self.human_robot.storage.storage_d - self.ai_robot.storage.storage_d

    def get_available_molecuse_e(self):
        return self.get_max_molecuse_e() - self.human_robot.storage.storage_e - self.ai_robot.storage.storage_e

    def get_enough_molecules_sample_size_in_cloud(self):
        return len(self.enough_molecuses_sample_id_list_for_human_robot)

    def get_one_enough_molecules_sample_id_in_cloud_for_human_robot(self):
        if len(self.enough_molecuses_sample_id_list_for_human_robot) > 0:
            return self.enough_molecuses_sample_id_list_for_human_robot[0]
        print("No sample can has enough molecuses in uploaded sample", file=sys.stderr)
        return None

    def can_cloud_sample_fetch_enough_molecules_for_human_robot(self, sample_id):
        if sample_id < 0:
            return False

        sample = self.cloud_sample.get_sample_by_id(sample_id)

        if sample is None:
            return False

        if sample.has_been_diagnosed() is False \
                or sample.should_be_uploaded(self.human_robot):
            return False

        need_storage = self.human_robot.get_sample_needed_storage(sample)

        if self.human_robot.storage.is_full():
            return False
        if need_storage.get_used_storage() == 0:
            return False

        if (0 < game.get_available_molecuse_a() <= need_storage.storage_a) \
                and (0 < game.get_available_molecuse_b() <= need_storage.storage_b) \
                and (0 < game.get_available_molecuse_c() <= need_storage.storage_c) \
                and (0 < game.get_available_molecuse_d() <= need_storage.storage_d) \
                and (0 < game.get_available_molecuse_e() <= need_storage.storage_e):
            return True

        return False

    def can_cloud_sample_fetch_more_molecules_for_human_robot(self, sample_id):
        if sample_id < 0:
            return False

        sample = self.cloud_sample.get_sample_by_id(sample_id)

        if sample is None:
            return False

        if sample.has_been_diagnosed() is False \
                or sample.should_be_uploaded(self.human_robot):
            return False

        need_storage = self.human_robot.get_sample_needed_storage(sample)

        if self.human_robot.storage.is_full():
            return False
        if need_storage.get_used_storage() == 0:
            return False

        if (game.get_available_molecuse_a() > 0 and need_storage.storage_a > 0) \
                or (game.get_available_molecuse_b() > 0 and need_storage.storage_b > 0) \
                or (game.get_available_molecuse_c() > 0 and need_storage.storage_c > 0) \
                or (game.get_available_molecuse_d() > 0 and need_storage.storage_d > 0) \
                or (game.get_available_molecuse_e() > 0 and need_storage.storage_e > 0):
            return True
        else:
            return False

    def get_sample_which_can_get_enough_molecuses_from_cloud(self):
        sample_list = []
        for i in range(self.cloud_sample.size()):
            if self.can_cloud_sample_fetch_enough_molecules_for_human_robot(
                    self.cloud_sample.get_sample_by_index(i).sample_id):
                sample_list.append(self.cloud_sample.get_sample_by_index(i))
        return sample_list

    def get_sample_size_which_can_get_enough_molecuses_from_cloud(self):
        return len(self.get_sample_which_can_get_enough_molecuses_from_cloud())

    def get_one_sample_id_which_can_get_enough_molecuses_from_cloud(self):
        sample_list = self.get_sample_which_can_get_enough_molecuses_from_cloud()
        if len(sample_list) != 0:
            return sample_list[0].sample_id
        return -1

    def get_sample_which_can_get_more_molecuses_from_cloud(self):
        sample_list = []
        for i in range(self.cloud_sample.size()):
            if self.can_cloud_sample_fetch_more_molecules_for_human_robot(
                    self.cloud_sample.get_sample_by_index(i).sample_id):
                sample_list.append(self.cloud_sample.get_sample_by_index(i))
        return sample_list

    def get_sample_size_which_can_get_more_molecuses(self):
        return len(self.get_sample_which_can_get_more_molecuses_from_cloud())

    def get_one_sample_which_can_get_more_molecuses_from_cloud(self):
        sample_list = self.get_sample_which_can_get_more_molecuses_from_cloud()
        if len(sample_list) != 0:
            return sample_list[0].sample_id
        return -1


game = Game()
my_robot = Robot(game, Robot.TYPE_HUMAN)
ai_robot = Robot(game, Robot.TYPE_AI)
game.set_human_robot(my_robot)
game.set_ai_robot(ai_robot)


def steps(from_position, to_position):
    if from_position == Module.EMPTY or to_position == Module.EMPTY:
        return 0
    elif from_position == Module.START_POS and to_position == Module.SAMPLES:
        return 2
    elif from_position == Module.START_POS and to_position == Module.DIAGNOSIS:
        return 2
    elif from_position == Module.START_POS and to_position == Module.MOLECULES:
        return 2
    elif from_position == Module.START_POS and to_position == Module.LABORATORY:
        return 2
    elif from_position == Module.START_POS and to_position == Module.START_POS:
        return 0
    elif from_position == Module.SAMPLES and to_position == Module.DIAGNOSIS:
        return 3
    elif from_position == Module.SAMPLES and to_position == Module.MOLECULES:
        return 3
    elif from_position == Module.SAMPLES and to_position == Module.LABORATORY:
        return 3
    elif from_position == Module.SAMPLES and to_position == Module.SAMPLES:
        return 0
    elif from_position == Module.DIAGNOSIS and to_position == Module.SAMPLES:
        return 3
    elif from_position == Module.DIAGNOSIS and to_position == Module.MOLECULES:
        return 3
    elif from_position == Module.DIAGNOSIS and to_position == Module.LABORATORY:
        return 4
    elif from_position == Module.DIAGNOSIS and to_position == Module.DIAGNOSIS:
        return 0
    elif from_position == Module.MOLECULES and to_position == Module.SAMPLES:
        return 3
    elif from_position == Module.MOLECULES and to_position == Module.DIAGNOSIS:
        return 3
    elif from_position == Module.MOLECULES and to_position == Module.LABORATORY:
        return 3
    elif from_position == Module.MOLECULES and to_position == Module.MOLECULES:
        return 0
    elif from_position == Module.LABORATORY and to_position == Module.SAMPLES:
        return 3
    elif from_position == Module.LABORATORY and to_position == Module.DIAGNOSIS:
        return 4
    elif from_position == Module.LABORATORY and to_position == Module.MOLECULES:
        return 3
    elif from_position == Module.LABORATORY and to_position == Module.LABORATORY:
        return 0
    else:
        return 0


def check_ai_robot_molecuse_spent():
    global my_robot
    global ai_robot


def should_jump_to_next_turn():
    global my_robot
    global ai_robot

    if my_robot.eta == 0:
        return False
    else:
        print("my_robot should do nothing in this turn", file=sys.stderr)
        print("go go go")
        return True


def fetch_molecules(sample_id):
    global my_robot
    global ai_robot
    global game

    print("DEBUG: try to get molecules for sample_id=", sample_id, file=sys.stderr)
    sample = my_robot.carrying_sample.get_sample_by_id(sample_id)
    need_storage = my_robot.get_sample_needed_storage(sample)

    if sample_id < -1:
        return

    if sample is not None:
        if (need_storage.storage_a > 0
                and game.get_available_molecuse_a() > 0):
            print("DEBUG: my_robot need", need_storage.storage_a, "A for sample_id=", sample_id, file=sys.stderr)
            print("CONNECT A")
            return
        elif (need_storage.storage_b > 0
              and game.get_available_molecuse_b() > 0):
            print("DEBUG: my_robot need", need_storage.storage_b, "B for sample_id=", sample_id, file=sys.stderr)
            print("CONNECT B")
            return
        elif (need_storage.storage_c > 0
              and game.get_available_molecuse_c() > 0):
            print("DEBUG: my_robot need", need_storage.storage_c, "C for sample_id=", sample_id, file=sys.stderr)
            print("CONNECT C")
            return
        elif (need_storage.storage_d > 0
              and game.get_available_molecuse_d() > 0):
            print("DEBUG: my_robot need", need_storage.storage_d, "D for sample_id=", sample_id, file=sys.stderr)
            print("CONNECT D")
            return
        elif (need_storage.storage_e > 0
              and game.get_available_molecuse_e() > 0):
            print("DEBUG: my_robot need", need_storage.storage_e, "E for sample_id=", sample_id, file=sys.stderr)
            print("CONNECT E")
            return
        else:
            print("DEBUG: please provide corrected sample_id=", sample_id, " to fetch molecuse", file=sys.stderr)
            return


def can_fetch_enough_molecuses(sample_id):
    global my_robot
    global ai_robot
    global game

    if sample_id < 0:
        return False

    if my_robot.storage.is_full():
        return False

    sample = my_robot.carrying_sample.get_sample_by_id(sample_id)

    need_storage = my_robot.get_sample_needed_storage(sample)
    if need_storage.is_empty():
        return False

    enough_molecuse_a = True
    enough_molecuse_b = True
    enough_molecuse_c = True
    enough_molecuse_d = True
    enough_molecuse_e = True

    if need_storage.storage_a > 0 \
            and game.get_available_molecuse_a() < need_storage.storage_a:
        enough_molecuse_a = False
    if need_storage.storage_b > 0 \
            and game.get_available_molecuse_b() < need_storage.storage_b:
        enough_molecuse_b = False
    if need_storage.storage_c > 0 \
            and game.get_available_molecuse_c() < need_storage.storage_c:
        enough_molecuse_c = False
    if need_storage.storage_d > 0 \
            and game.get_available_molecuse_d() < need_storage.storage_d:
        enough_molecuse_d = False
    if need_storage.storage_e > 0 \
            and game.get_available_molecuse_e() < need_storage.storage_e:
        enough_molecuse_e = False

    if enough_molecuse_a \
            and enough_molecuse_b \
            and enough_molecuse_c \
            and enough_molecuse_d \
            and enough_molecuse_e:
        return True

    return False


def can_fetch_more_molecules(sample_id):
    global my_robot
    global ai_robot
    global game

    if sample_id < 0:
        return False

    sample = my_robot.carrying_sample.get_sample_by_id(sample_id)
    need_storage = my_robot.get_sample_needed_storage(sample)

    if my_robot.storage.is_full():
        return False
    if need_storage.is_empty():
        return False

    if (game.get_available_molecuse_a() > 0 and need_storage.storage_a > 0) \
            or (game.get_available_molecuse_b() > 0 and need_storage.storage_b > 0) \
            or (game.get_available_molecuse_c() > 0 and need_storage.storage_c > 0) \
            or (game.get_available_molecuse_d() > 0 and need_storage.storage_d > 0) \
            or (game.get_available_molecuse_e() > 0 and need_storage.storage_e > 0):
        return True
    else:
        return False


def get_sample_size_which_can_fetch_enough_molecuses():
    global my_robot
    global ai_robot
    global game

    count = 0

    for i in range(my_robot.carrying_sample.size()):
        sample = my_robot.carrying_sample.get_sample_by_index(i)
        if can_fetch_enough_molecuses(sample.sample_id):
            count = count + 1

    return count


def need_to_upload_sample_for_enough_sample_downloading():
    global my_robot
    global ai_robot
    global game

    empty_sample_number = SampleList.MAX_CARRIED_SAMPLE_NUM - my_robot.carrying_sample.size()
    real_no_used_sample_number = my_robot.carrying_sample.size() - my_robot.get_enough_molecuses_sample_size()

    if my_robot.carrying_sample.is_empty():
        return False

    if game.get_enough_molecules_sample_size_in_cloud() > 0:
        if (game.get_enough_molecules_sample_size_in_cloud() - empty_sample_number) > 0 \
                and real_no_used_sample_number > 0:
            return True
    return False


def need_to_upload_sample_for_can_fetch_enough_sample_downloading():
    global my_robot
    global ai_robot
    global game
    empty_sample_number = SampleList.MAX_CARRIED_SAMPLE_NUM - my_robot.carrying_sample.size()
    real_no_used_sample_number = my_robot.carrying_sample.size() \
                                 - my_robot.get_enough_molecuses_sample_size() \
                                 - get_sample_size_which_can_fetch_enough_molecuses()

    if my_robot.carrying_sample.is_empty():
        return False

    if game.get_sample_size_which_can_get_enough_molecuses_from_cloud() > 0:
        if (game.get_sample_size_which_can_get_enough_molecuses_from_cloud() - empty_sample_number) > 0 \
                and real_no_used_sample_number > 0:
            return True

    return False


def need_to_download_enough_molecuses_sample_from_cloud():
    global my_robot
    global ai_robot
    global game

    if my_robot.carrying_sample.is_full() is False \
            and game.get_enough_molecules_sample_size_in_cloud() != 0:
        return True

    return False


def need_to_download_which_can_get_enough_molecuses_sample_from_cloud():
    global my_robot
    global ai_robot
    global game

    if need_to_download_enough_molecuses_sample_from_cloud():
        return False

    if my_robot.carrying_sample.is_full() is False \
            and game.get_sample_size_which_can_get_enough_molecuses_from_cloud() != 0:
        return True
    return False


def need_to_download_which_can_get_more_molecuses_sample_from_cloud():
    global my_robot
    global ai_robot
    global game

    if need_to_download_which_can_get_enough_molecuses_sample_from_cloud():
        return False

    if need_to_download_enough_molecuses_sample_from_cloud():
        return False

    # check can download which can get more molecuses sample
    if game.get_sample_size_which_can_get_more_molecuses() != 0 \
            and my_robot.carrying_sample.is_full() is False:
        return True
    return False


def need_to_download_sample_from_cloud():
    global my_robot
    global ai_robot
    global game

    # check can download enough molecuses sample
    if need_to_download_enough_molecuses_sample_from_cloud():
        return True
    if need_to_download_which_can_get_enough_molecuses_sample_from_cloud():
        return True
    return False


def get_sample_id_which_can_fetch_enough_molecuses():
    global my_robot
    global ai_robot
    global game

    for i in range(my_robot.carrying_sample.size()):
        sample = my_robot.carrying_sample.get_sample_by_index(i)
        if can_fetch_enough_molecuses(sample.sample_id):
            return sample.sample_id

    return -1


def get_sample_id_which_can_not_fetch_enough_molecuses():
    global my_robot
    global ai_robot
    global game

    for i in range(my_robot.carrying_sample.size()):
        sample = my_robot.carrying_sample.get_sample_by_index(i)
        if my_robot.has_sample_got_enough_molecuse(sample) is False \
                and can_fetch_enough_molecuses(sample.sample_id) is False:
            return sample.sample_id

    return -1


def get_sample_id_which_can_fetch_more_molecuses():
    global my_robot
    global ai_robot
    global game

    for i in range(my_robot.carrying_sample.size()):
        sample = my_robot.carrying_sample.get_sample_by_index(i)
        if can_fetch_more_molecules(sample.sample_id):
            return sample.sample_id

    return -1


def get_type_of_molecuse_to_block_ai_robot():
    global my_robot
    global ai_robot
    global game

    if my_robot.storage.is_full() or my_robot.expertise.get_total_expertise() < 7:
        return ''

    needed_storage = ai_robot.get_best_block_storage_in_all_sample()
    if needed_storage.get_used_storage == 0:
        return ''

    my_robot_step_to_module = steps(my_robot.current_target, Module.MOLECULES)
    ai_robot_step_to_module = steps(ai_robot.current_target, Module.MOLECULES)

    if 0 < needed_storage.storage_a <= game.get_available_molecuse_a():
        my_robot_execution_step = my_robot_step_to_module + game.get_available_molecuse_a() - needed_storage.storage_a + 1
        ai_robot_execution_step = ai_robot_step_to_module + needed_storage.storage_a
        if my_robot.storage.storage_a + (
                game.get_available_molecuse_a() - needed_storage.storage_a + 1) <= game.get_max_molecuse_a() \
                and my_robot.storage.get_used_storage() + (
                    game.get_available_molecuse_a() - needed_storage.storage_a + 1) <= Storage.MAX_TOTAL_STORAGE_NUM \
                and my_robot_execution_step <= ai_robot_execution_step:
            return 'A'
    if 0 < needed_storage.storage_b <= game.get_available_molecuse_b():
        my_robot_execution_step = my_robot_step_to_module + game.get_available_molecuse_b() - needed_storage.storage_b + 1
        ai_robot_execution_step = ai_robot_step_to_module + needed_storage.storage_b
        if my_robot.storage.storage_b + (
                game.get_available_molecuse_b() - needed_storage.storage_b + 1) <= game.get_max_molecuse_b() \
                and my_robot.storage.get_used_storage() + (
                    game.get_available_molecuse_b() - needed_storage.storage_b + 1) <= Storage.MAX_TOTAL_STORAGE_NUM \
                and my_robot_execution_step <= ai_robot_execution_step:
            return 'B'
    if 0 < needed_storage.storage_c <= game.get_available_molecuse_c():
        my_robot_execution_step = my_robot_step_to_module + game.get_available_molecuse_c() - needed_storage.storage_c + 1
        ai_robot_execution_step = ai_robot_step_to_module + needed_storage.storage_c
        if my_robot.storage.storage_c + (
                game.get_available_molecuse_c() - needed_storage.storage_c + 1) <= game.get_max_molecuse_c() \
                and my_robot.storage.get_used_storage() + (
                    game.get_available_molecuse_c() - needed_storage.storage_c + 1) <= Storage.MAX_TOTAL_STORAGE_NUM \
                and my_robot_execution_step <= ai_robot_execution_step:
            return 'C'
    if 0 < needed_storage.storage_d <= game.get_available_molecuse_d():
        my_robot_execution_step = my_robot_step_to_module + game.get_available_molecuse_d() - needed_storage.storage_d + 1
        ai_robot_execution_step = ai_robot_step_to_module + needed_storage.storage_d
        if my_robot.storage.storage_d + (
                game.get_available_molecuse_d() - needed_storage.storage_d + 1) <= game.get_max_molecuse_d() \
                and my_robot.storage.get_used_storage() + (
                    game.get_available_molecuse_d() - needed_storage.storage_d + 1) <= Storage.MAX_TOTAL_STORAGE_NUM \
                and my_robot_execution_step <= ai_robot_execution_step:
            return 'D'
    if 0 < needed_storage.storage_e <= game.get_available_molecuse_e():
        my_robot_execution_step = my_robot_step_to_module + game.get_available_molecuse_e() - needed_storage.storage_e + 1
        ai_robot_execution_step = ai_robot_step_to_module + needed_storage.storage_e
        if my_robot.storage.storage_e + (
                game.get_available_molecuse_e() - needed_storage.storage_e + 1) <= game.get_max_molecuse_e() \
                and my_robot.storage.get_used_storage() + (
                    game.get_available_molecuse_e() - needed_storage.storage_e + 1) <= Storage.MAX_TOTAL_STORAGE_NUM \
                and my_robot_execution_step <= ai_robot_execution_step:
            return 'E'

    return ''


def generate_rank():
    global my_robot
    global ai_robot
    global game

    unconsumed_storage = my_robot.get_unconsumed_storage()

    if my_robot.expertise.get_total_expertise() >= 10:
        if my_robot.carrying_sample.size() == 1 and unconsumed_storage.get_used_storage() >= 7:
            return 1
        elif my_robot.carrying_sample.size() == 2 and unconsumed_storage.get_used_storage() >= 4:
            return 2
        else:
            return 3
    elif my_robot.expertise.get_total_expertise() >= 7:
        if my_robot.carrying_sample.size() == 1 and unconsumed_storage.get_used_storage() >= 7:
            return 1
        elif my_robot.carrying_sample.size() == 2 and unconsumed_storage.get_used_storage() >= 4:
            return 1
        else:
            return 2
    else:
        return 1


def prepare():
    global my_robot
    global ai_robot
    global game

    game.prepare()
    my_robot.prepare()
    ai_robot.prepare()


def clean_up():
    global my_robot
    global ai_robot
    global game

    my_robot.clean_up()
    ai_robot.clean_up()
    game.clean_up()


##############################################################################################
def go_to_samples():
    global my_robot
    global ai_robot

    sample_id_can_fetch_enough_molecuse = get_sample_id_which_can_fetch_enough_molecuses()
    sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()
    enough_molecuse_sample_size = my_robot.get_enough_molecuses_sample_size()
    type_of_molecuse_to_block_ai_robot = get_type_of_molecuse_to_block_ai_robot()

    if my_robot.current_target == Module.START_POS:
        # game start
        print("DEBUG: my robot go to SAMPLES", file=sys.stderr)
        print("GOTO SAMPLES")
    elif my_robot.previous_target == Module.LABORATORY and my_robot.current_target == Module.LABORATORY:
        if sample_id_should_fetch_molecuse == -1 \
                and my_robot.get_enough_molecuses_sample_size() == 0 \
                and type_of_molecuse_to_block_ai_robot == '':
            print("DEBUG: my robot go to SAMPLES due to all enough sample are extracted "
                  "and NO sample can get enough molecuse", file=sys.stderr)
            print("GOTO SAMPLES")
    elif my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.DIAGNOSIS:
        if my_robot.carrying_sample.is_empty() \
                and need_to_download_sample_from_cloud() is False:
            print("DEBUG: my robot go to SAMPLES dut to carrying sample empty", file=sys.stderr)
            print("GOTO SAMPLES")
    elif my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.MOLECULES:
        if sample_id_should_fetch_molecuse != -1:
            if can_fetch_more_molecules(sample_id_should_fetch_molecuse) is False:
                if my_robot.storage.is_full() and my_robot.carrying_sample.is_full() is False:
                    print("DEBUG: my robot go to SAMPLES dut to storage full and carrying sample not full",
                          file=sys.stderr)
                    print("GOTO SAMPLES")
        else:
            if my_robot.carrying_sample.is_full() is False \
                    and enough_molecuse_sample_size == 0 \
                    and type_of_molecuse_to_block_ai_robot == '':
                print(
                    "DEBUG: my robot go to SAMPLES dut to carrying sample not full and no more molecuses can be fetched",
                    file=sys.stderr)
                print("GOTO SAMPLES")
            elif my_robot.carrying_sample.is_empty() \
                    and get_type_of_molecuse_to_block_ai_robot() == '':
                print("DEBUG: my robot go to SAMPLES dut to carrying sample empty",
                      file=sys.stderr)
                print("GOTO SAMPLES")


def go_to_diagnosis():
    global my_robot
    global ai_robot

    sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()

    if my_robot.previous_target == Module.SAMPLES and my_robot.current_target == Module.SAMPLES:
        if my_robot.carrying_sample.is_full():
            print("DEBUG: my robot go to DIAGNOSIS", file=sys.stderr)
            print("GOTO DIAGNOSIS")
    elif my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.MOLECULES:
        if my_robot.get_enough_molecuses_sample_size() == 0:
            if sample_id_should_fetch_molecuse == -1:
                if my_robot.carrying_sample.is_full():
                    print("DEBUG: my robot go to DIAGNOSIS due to no enough molecuse", file=sys.stderr)
                    print("GOTO DIAGNOSIS")
            else:
                if my_robot.storage.is_full() and my_robot.carrying_sample.is_full():
                    print("DEBUG: my robot go to DIAGNOSIS due to storage is full", file=sys.stderr)
                    print("GOTO DIAGNOSIS")


def go_to_molecules():
    global my_robot
    global ai_robot
    global game

    sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()
    sample_id_can_fetch_enough_molecuse = get_sample_id_which_can_fetch_enough_molecuses()
    type_of_molecuse_to_block_ai_robot = get_type_of_molecuse_to_block_ai_robot()

    if my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.DIAGNOSIS:
        if my_robot.carrying_sample.get_undiagnosed_sample_id() == -1 \
                and my_robot.carrying_sample.get_being_uploaded_sample_id(my_robot, ai_robot) == -1\
                and need_to_upload_sample_for_can_fetch_enough_sample_downloading() is False \
                and need_to_upload_sample_for_enough_sample_downloading() is False:
            if my_robot.carrying_sample.is_full() \
                    and my_robot.get_enough_molecuses_sample_size() < my_robot.carrying_sample.size() \
                    and sample_id_should_fetch_molecuse != -1 \
                    and need_to_download_sample_from_cloud() is False:
                print("DEBUG: my robot go to MOLECULES due to due to one of carrying sample can fetch molecuse",
                      file=sys.stderr)
                print("GOTO MOLECULES")
            elif my_robot.carrying_sample.is_full() is False \
                    and my_robot.carrying_sample.is_empty() is False \
                    and sample_id_should_fetch_molecuse != -1 \
                    and my_robot.carrying_sample.get_undiagnosed_sample_id() == -1 \
                    and my_robot.carrying_sample.get_being_uploaded_sample_id(my_robot, ai_robot) == -1 \
                    and need_to_download_sample_from_cloud() is False:
                print("DEBUG: my robot go to MOLECULES due to due to NO sample can be download from cloud",
                      file=sys.stderr)
                print("GOTO MOLECULES")
    elif my_robot.previous_target == Module.LABORATORY and my_robot.current_target == Module.LABORATORY:
        if sample_id_should_fetch_molecuse != -1 \
                and my_robot.get_enough_molecuses_sample_size() == 0:
            print("DEBUG: my robot go to MOLECULES due to sample can fetch molecuse and NO sample can be extracted",
                  file=sys.stderr)
            print("GOTO MOLECULES")
        elif get_type_of_molecuse_to_block_ai_robot() != '' \
                and my_robot.get_enough_molecuses_sample_size() == 0:
            print("DEBUG: my robot go to MOLECULES due to can block ai robot and NO sample can be extracted",
                  file=sys.stderr)
            print("GOTO MOLECULES")


def go_to_laboratory():
    global my_robot
    global ai_robot
    global game

    sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()
    type_of_molecuse_to_block_ai_robot = get_type_of_molecuse_to_block_ai_robot()

    if my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.MOLECULES:
        if sample_id_should_fetch_molecuse == -1:
            if my_robot.get_enough_molecuses_sample_size() > 0:
                if my_robot.carrying_sample.is_full():
                    print("DEBUG: my robot go to LABORATORY due to No sample can get molecuse", file=sys.stderr)
                    print("GOTO LABORATORY")
                elif type_of_molecuse_to_block_ai_robot == '':
                    print("DEBUG: my robot go to LABORATORY due to No sample can get molecuse", file=sys.stderr)
                    print("GOTO LABORATORY")
    elif my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.MOLECULES:
        if sample_id_should_fetch_molecuse == -1 \
                and my_robot.get_enough_molecuses_sample_size() > 0:
            print("DEBUG: my robot go to LABORATORY", file=sys.stderr)
            print("GOTO LABORATORY")
    elif (my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.DIAGNOSIS) \
            or (my_robot.previous_target == Module.SAMPLES and my_robot.current_target == Module.DIAGNOSIS):
        if my_robot.carrying_sample.get_undiagnosed_sample_id() == -1 \
                and my_robot.carrying_sample.get_being_uploaded_sample_id(my_robot, ai_robot) == -1 \
                and need_to_upload_sample_for_enough_sample_downloading() is False \
                and need_to_upload_sample_for_can_fetch_enough_sample_downloading() is False \
                and need_to_download_sample_from_cloud() is False:
            if my_robot.get_enough_molecuses_sample_size() == my_robot.carrying_sample.size() \
                    and my_robot.carrying_sample.size() > 0 \
                    and need_to_download_sample_from_cloud() is False:
                print("DEBUG: my robot go to LABORATORY due to all sample have enough molecuses", file=sys.stderr)
                print("GOTO LABORATORY")
            elif my_robot.get_enough_molecuses_sample_size() > 0 \
                    and sample_id_should_fetch_molecuse == -1 \
                    and need_to_download_sample_from_cloud() is False:
                print("DEBUG: my robot go to LABORATORY due to some sample have enough molecuses "
                      "and other sample can not fetch molecuse", file=sys.stderr)
                print("GOTO LABORATORY")
            elif my_robot.get_enough_molecuses_sample_size() > 0 \
                    and my_robot.storage.is_full():
                print("DEBUG: my robot go to LABORATORY due to some sample have enough molecuses "
                      "and storage full", file=sys.stderr)
                print("GOTO LABORATORY")


#################################################################################################
def get_rank():
    global my_robot
    global ai_robot

    rank = generate_rank()

    if my_robot.previous_target == Module.START_POS:
        if my_robot.carrying_sample.is_full() is False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif my_robot.previous_target == Module.SAMPLES and my_robot.current_target == Module.SAMPLES:
        if my_robot.carrying_sample.is_full() is False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif my_robot.previous_target == Module.LABORATORY and my_robot.current_target == Module.SAMPLES:
        if my_robot.carrying_sample.is_full() is False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.SAMPLES:
        if my_robot.carrying_sample.is_full() is False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.SAMPLES:
        if my_robot.carrying_sample.is_full() is False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)


def get_diagnose():
    global my_robot
    global ai_robot

    if my_robot.previous_target == Module.SAMPLES and my_robot.current_target == Module.DIAGNOSIS:
        undiagnosed_sample_id = my_robot.carrying_sample.get_undiagnosed_sample_id()
        if undiagnosed_sample_id > -1:
            print("DEBUG: my robot diagnose sample id", undiagnosed_sample_id, file=sys.stderr)
            print("CONNECT ", undiagnosed_sample_id)
    elif my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.DIAGNOSIS:
        undiagnosed_sample_id = my_robot.carrying_sample.get_undiagnosed_sample_id()
        if undiagnosed_sample_id > -1:
            print("DEBUG: my robot diagnose sample id", undiagnosed_sample_id, file=sys.stderr)
            print("CONNECT ", undiagnosed_sample_id)


def upload_sample():
    global my_robot
    global ai_robot
    global game

    if (my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.DIAGNOSIS) \
            or (my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.DIAGNOSIS) \
            or (my_robot.previous_target == Module.SAMPLES and my_robot.current_target == Module.DIAGNOSIS):
        sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()

        if my_robot.carrying_sample.get_undiagnosed_sample_id() == -1:
            uploaded_sample_id = my_robot.carrying_sample.get_being_uploaded_sample_id(my_robot, ai_robot)
            if uploaded_sample_id > -1:
                print("DEBUG: my robot upload sample id", uploaded_sample_id, " due to its cost", file=sys.stderr)
                my_robot.carrying_sample.mark_sample_need_to_be_deleted(uploaded_sample_id)
                print("CONNECT ", uploaded_sample_id)
            elif uploaded_sample_id == -1:
                if sample_id_should_fetch_molecuse == -1 \
                        and my_robot.get_enough_molecuses_sample_size() == 0 \
                        and my_robot.carrying_sample.is_empty() is False \
                        and (need_to_download_sample_from_cloud() is False):
                    needed_upload_id = get_sample_id_which_can_not_fetch_enough_molecuses()
                    if needed_upload_id != -1:
                        print("DEBUG: my robot upload sample id", needed_upload_id,
                              "due to there are samples can not fetch enough molecuses",
                              file=sys.stderr)
                        my_robot.carrying_sample.mark_sample_need_to_be_deleted(needed_upload_id)
                        print("CONNECT ", needed_upload_id)
                elif sample_id_should_fetch_molecuse != -1 \
                        and (need_to_upload_sample_for_can_fetch_enough_sample_downloading()
                             or need_to_upload_sample_for_enough_sample_downloading()):
                    print("DEBUG: my robot upload sample id", sample_id_should_fetch_molecuse,
                          "due to enough or can fetch enough molecuses sample in cloud", file=sys.stderr)
                    my_robot.carrying_sample.mark_sample_need_to_be_deleted(sample_id_should_fetch_molecuse)
                    print("CONNECT ", sample_id_should_fetch_molecuse)
                elif sample_id_should_fetch_molecuse == -1 \
                        and (need_to_upload_sample_for_can_fetch_enough_sample_downloading()
                             or need_to_upload_sample_for_enough_sample_downloading()):
                    needed_upload_id = get_sample_id_which_can_not_fetch_enough_molecuses()
                    if needed_upload_id != -1:
                        print("DEBUG: my robot upload sample id", needed_upload_id,
                              "due to enough or can fetch enough molecuses sample in cloud", file=sys.stderr)
                        my_robot.carrying_sample.mark_sample_need_to_be_deleted(needed_upload_id)
                        print("CONNECT ", needed_upload_id)


def download_sample():
    global my_robot
    global ai_robot
    global game

    if my_robot.carrying_sample.get_undiagnosed_sample_id() != -1 \
            or my_robot.carrying_sample.get_being_uploaded_sample_id(my_robot, ai_robot) != -1:
        return

    sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()

    if (my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.DIAGNOSIS) \
            or (my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.DIAGNOSIS):
        if need_to_upload_sample_for_enough_sample_downloading() is False \
                and need_to_upload_sample_for_can_fetch_enough_sample_downloading() is False \
                and need_to_download_enough_molecuses_sample_from_cloud() \
                and my_robot.carrying_sample.is_full() is False:
            sample_id = game.get_one_enough_molecules_sample_id_in_cloud_for_human_robot()
            print("DEBUG: my robot download sample id", sample_id,
                  "due to enough molecuses sample in cloud", file=sys.stderr)
            print("CONNECT ", sample_id)
        elif need_to_upload_sample_for_enough_sample_downloading() is False \
                and need_to_upload_sample_for_can_fetch_enough_sample_downloading() is False \
                and need_to_download_which_can_get_enough_molecuses_sample_from_cloud() \
                and my_robot.carrying_sample.is_full() is False:
            sample_id = game.get_one_sample_id_which_can_get_enough_molecuses_from_cloud()
            print("DEBUG: my robot download sample id", sample_id,
                  "due to can get enough molecuses sample in cloud", file=sys.stderr)
            print("CONNECT ", sample_id)


def get_molecules():
    global my_robot
    global ai_robot
    global game

    sample_id_can_fetch_enough_molecuse = get_sample_id_which_can_fetch_enough_molecuses()
    sample_id_should_fetch_molecuse = get_sample_id_which_can_fetch_more_molecuses()
    type_of_molecuse_to_block_ai_robot = get_type_of_molecuse_to_block_ai_robot()

    if my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.MOLECULES:
        if sample_id_should_fetch_molecuse != -1:
            if can_fetch_more_molecules(sample_id_should_fetch_molecuse):
                fetch_molecules(sample_id_should_fetch_molecuse)
            else:
                if my_robot.storage.is_full() is False \
                        and my_robot.get_enough_molecuses_sample_size() == 0:
                    print("DEBUG: my robot should wait due to not enough molecuse", file=sys.stderr)
                    print("WAIT")
    elif my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.MOLECULES:
        if sample_id_should_fetch_molecuse != -1:
            if can_fetch_more_molecules(sample_id_should_fetch_molecuse):
                fetch_molecules(sample_id_should_fetch_molecuse)
            else:
                if my_robot.storage.is_full() is False \
                        and my_robot.get_enough_molecuses_sample_size() == 0:
                    print("DEBUG: my robot should wait due to not enough molecuse", file=sys.stderr)
                    print("WAIT")
        elif sample_id_should_fetch_molecuse == -1 \
                and type_of_molecuse_to_block_ai_robot != '' \
                and my_robot.carrying_sample.is_full() is False:
            print("DEBUG: my robot fetch 1 molecuse ", type_of_molecuse_to_block_ai_robot,
                  " to block ai robot", file=sys.stderr)
            print("CONNECT", type_of_molecuse_to_block_ai_robot)
    elif my_robot.previous_target == Module.LABORATORY and my_robot.current_target == Module.MOLECULES:
        if sample_id_should_fetch_molecuse != -1:
            fetch_molecules(sample_id_should_fetch_molecuse)
        elif type_of_molecuse_to_block_ai_robot != '':
            print("DEBUG: my robot fetch 1 molecuse ", type_of_molecuse_to_block_ai_robot,
                  " to block ai robot", file=sys.stderr)
            print("CONNECT", type_of_molecuse_to_block_ai_robot)


def extract_medicine():
    global my_robot
    global ai_robot
    global game

    sample_id = my_robot.get_one_enough_molecules_sample_id()

    if my_robot.previous_target == Module.MOLECULES and my_robot.current_target == Module.LABORATORY:
        if sample_id != -1:
            print("DEBUG: my robot extract medicine for sample id", sample_id, file=sys.stderr)
            my_robot.carrying_sample.mark_sample_need_to_be_deleted(sample_id)
            print("CONNECT ", sample_id)
    elif my_robot.previous_target == Module.DIAGNOSIS and my_robot.current_target == Module.LABORATORY:
        if sample_id != -1:
            print("DEBUG: my robot extract medicine for sample id", sample_id, file=sys.stderr)
            my_robot.mark_sample_need_to_be_deleted(sample_id)
            print("CONNECT ", sample_id)
    elif my_robot.previous_target == Module.LABORATORY and my_robot.current_target == Module.LABORATORY:
        if sample_id != -1:
            print("DEBUG: my robot extract medicine for sample id", sample_id, file=sys.stderr)
            my_robot.carrying_sample.mark_sample_need_to_be_deleted(sample_id)
            print("CONNECT ", sample_id)


#############################################################################
project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]
    game.add_science_project(ScienceProject(i, a, b, c, d, e))

# game loop
while True:
    for i in range(2):
        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
        eta = int(eta)
        score = int(score)
        storage_a = int(storage_a)
        storage_b = int(storage_b)
        storage_c = int(storage_c)
        storage_d = int(storage_d)
        storage_e = int(storage_e)
        expertise_a = int(expertise_a)
        expertise_b = int(expertise_b)
        expertise_c = int(expertise_c)
        expertise_d = int(expertise_d)
        expertise_e = int(expertise_e)

        if i == 0:
            current_target = target
            print("my_robot previous_target is ", my_robot.previous_target,
                  ", current_target is ", my_robot.current_target,
                  file=sys.stderr)
            print("my_robot eta is", eta,
                  ", score is", score,
                  file=sys.stderr)
            print("my_robot expertise_a is", expertise_a,
                  ", expertise_b is", expertise_b,
                  ", expertise_c is", expertise_c,
                  ", expertise_d is", expertise_d,
                  ", expertise_e is", expertise_e,
                  file=sys.stderr)
            print("storage.storage_a is", storage_a,
                  ", storage.storage_b is", storage_b,
                  ", storage.storage_c is", storage_c,
                  ", storage.storage_d is", storage_d,
                  ", storage.storage_e is", storage_e,
                  file=sys.stderr)
            my_robot.set_current_target(target)
            my_robot.set_eta(eta)
            my_robot.set_score(score)
            my_robot.storage.storage_a = storage_a
            my_robot.storage.storage_b = storage_b
            my_robot.storage.storage_c = storage_c
            my_robot.storage.storage_d = storage_d
            my_robot.storage.storage_e = storage_e
            my_robot.expertise.expertise_a = expertise_a
            my_robot.expertise.expertise_b = expertise_b
            my_robot.expertise.expertise_c = expertise_c
            my_robot.expertise.expertise_d = expertise_d
            my_robot.expertise.expertise_e = expertise_e
        elif i == 1:
            current_target = target
            ai_robot.set_current_target(target)
            ai_robot.set_eta(eta)
            ai_robot.set_score(score)
            ai_robot.storage.storage_a = storage_a
            ai_robot.storage.storage_b = storage_b
            ai_robot.storage.storage_c = storage_c
            ai_robot.storage.storage_d = storage_d
            ai_robot.storage.storage_e = storage_e
            ai_robot.expertise.expertise_a = expertise_a
            ai_robot.expertise.expertise_b = expertise_b
            ai_robot.expertise.expertise_c = expertise_c
            ai_robot.expertise.expertise_d = expertise_d
            ai_robot.expertise.expertise_e = expertise_e
            print("ai_robot previous_target is ", ai_robot.previous_target,
                  ", current_target is ", ai_robot.current_target,
                  file=sys.stderr)
            print("ai_robot eta is", eta, ", score is", score, file=sys.stderr)
            print("ai_robot expertise_a is", expertise_a, ", expertise_b is", expertise_b, ", expertise_c is",
                  expertise_c,
                  ", expertise_d is", expertise_d, ", expertise_e is", expertise_e, file=sys.stderr)
            print("storage.storage_a is", storage_a,
                  ", storage.storage_b is", storage_b,
                  ", storage.storage_c is", storage_c,
                  ", storage.storage_d is", storage_d,
                  ", storage.storage_e is", storage_e,
                  file=sys.stderr)
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]

    sample_count = int(input())

    print("sample_count", sample_count, file=sys.stderr)

    for i in range(sample_count):
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
        sample_id = int(sample_id)
        carried_by = int(carried_by)
        rank = int(rank)
        health = int(health)
        cost_a = int(cost_a)
        cost_b = int(cost_b)
        cost_c = int(cost_c)
        cost_d = int(cost_d)
        cost_e = int(cost_e)
        total_cost = cost_a + cost_b + cost_c + cost_d + cost_e

        if carried_by == 0:
            my_robot.carrying_sample.add_sample(
                Sample(game, sample_id, carried_by, health, rank, expertise_gain, total_cost, cost_a, cost_b, cost_c,
                       cost_d, cost_e))

        if carried_by == 1:
            ai_robot.carrying_sample.add_sample(
                Sample(game, sample_id, carried_by, health, rank, expertise_gain, total_cost, cost_a, cost_b, cost_c,
                       cost_d, cost_e))

        if carried_by == -1:
            game.cloud_sample.add_sample(
                Sample(game, sample_id, carried_by, health, rank, expertise_gain, total_cost, cost_a, cost_b, cost_c,
                       cost_d, cost_e))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    prepare()
    if should_jump_to_next_turn() is False:
        go_to_samples()
        get_rank()

        go_to_diagnosis()
        get_diagnose()
        upload_sample()
        download_sample()

        go_to_molecules()
        get_molecules()

        go_to_laboratory()
        extract_medicine()

    clean_up()
