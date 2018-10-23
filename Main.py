import sys
import math


# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
class ScienceProject:
    def __init__(self, project_id, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e):
        self.project_id = project_id
        self.expertise_a = expertise_a
        self.expertise_b = expertise_b
        self.expertise_c = expertise_c
        self.expertise_d = expertise_d
        self.expertise_e = expertise_e
        self.total_expertise = expertise_a + expertise_b + expertise_c + expertise_d + expertise_e

        print("Debug: new a sciense project, project_id", self.project_id,
              ",expertise_a", self.expertise_a,
              ",expertise_b", self.expertise_b, \
              ",expertise_c", self.expertise_c, \
              ",expertise_d ", self.expertise_d, \
              ",expertise_e ", self.expertise_e, \
              ",total_expertise ", self.total_expertise, \
              file=sys.stderr)


class Game:
    INIT_MAX_MOLECUSE_NUMBER = 5

    def __init__(self):
        self.turn = -1
        self.uploaded_sample = []
        self.scienceProjects = []

        self.additional_mollecuse_a = 0
        self.additional_mollecuse_b = 0
        self.additional_mollecuse_c = 0
        self.additional_mollecuse_d = 0
        self.additional_mollecuse_e = 0

        self.rank_count = 0

    def cleanUp(self):
        return

    def addScienceProject(self, scienceProject):
        self.scienceProjects.append(scienceProject)

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

    def add_uploaded_sample(self, sample):
        for i in range(len(self.uploaded_sample)):
            if sample.sample_id == self.uploaded_sample[i].sample_id:
                self.uploaded_sample.remove(self.uploaded_sample[i])
                break

        for i in range(len(self.uploaded_sample)):
            if sample.total_cost < self.uploaded_sample[i].total_cost:
                self.uploaded_sample.insert(i, sample)
                print("Debug: insert sample id", sample.sample_id, "at ", i, " in uploaded sample", file=sys.stderr)
                return

        print("Debug: append sample id", sample.sample_id, "in uploaded sample", file=sys.stderr)
        self.uploaded_sample.append(sample)

    def deleteUploadedSample(self, sample_id):
        for i in range(len(self.uploaded_sample)):
            if sample_id == self.uploaded_sample[i].sample_id:
                self.uploaded_sample.remove(self.uploaded_sample[i])
                print("Debug: sample id", sample_id, " has been deleted from uploaded sample", file=sys.stderr)
                return

    def getSampleIdWhichCanFetchEnoughMoleculesFromModuleInUploadedSample(self, humanRobot, aiRobot):
        for i in range(len(self.uploaded_sample)):
            molecuse_a_enough = True
            molecuse_b_enough = True
            molecuse_c_enough = True
            molecuse_d_enough = True
            molecuse_e_enough = True

            if self.uploaded_sample[i].cost_a > 0 \
                    and (self.uploaded_sample[i].cost_a - humanRobot.storage_a - humanRobot.expertise_a) > 0 \
                    and (self.get_max_molecuse_a() - aiRobot.storage_a - humanRobot.storage_a) <= 0:
                print("Debug: molecuse A is not enough for ", self.uploaded_sample[i].sample_id, file=sys.stderr)
                molecuse_a_enough = False

            if self.uploaded_sample[i].cost_b > 0 \
                    and (self.uploaded_sample[i].cost_b - humanRobot.storage_b - humanRobot.expertise_b) > 0 \
                    and (self.get_max_molecuse_b() - aiRobot.storage_b - humanRobot.storage_b) <= 0:
                print("Debug: molecuse B is not enough for ", self.uploaded_sample[i].sample_id, file=sys.stderr)
                molecuse_b_enough = False

            if self.uploaded_sample[i].cost_c > 0 \
                    and (self.uploaded_sample[i].cost_c - humanRobot.storage_c - humanRobot.expertise_c) > 0 \
                    and (self.get_max_molecuse_c() - aiRobot.storage_c - humanRobot.storage_c) <= 0:
                print("Debug: molecuse C is not enough for ", self.uploaded_sample[i].sample_id, file=sys.stderr)
                molecuse_c_enough = False

            if self.uploaded_sample[i].cost_d > 0 \
                    and (self.uploaded_sample[i].cost_d - humanRobot.storage_d - humanRobot.expertise_d) > 0 \
                    and (self.get_max_molecuse_d() - aiRobot.storage_d - humanRobot.storage_d) <= 0:
                print("Debug: molecuse D is not enough for ", self.uploaded_sample[i].sample_id, file=sys.stderr)
                molecuse_d_enough = False

            if self.uploaded_sample[i].cost_e > 0 \
                    and (self.uploaded_sample[i].cost_e - humanRobot.storage_e - humanRobot.expertise_e) > 0 \
                    and (self.get_max_molecuse_e() - aiRobot.storage_e - humanRobot.storage_e) <= 0:
                print("Debug: molecuse D is not enough for ", self.uploaded_sample[i].sample_id, file=sys.stderr)
                molecuse_e_enough = False

            if molecuse_a_enough == True \
                    and molecuse_b_enough == True \
                    and molecuse_c_enough == True \
                    and molecuse_d_enough == True \
                    and molecuse_e_enough == True \
                    and self.uploaded_sample[i].shouldBeUploaded(humanRobot) == False:
                print("Debug: find sample id", self.uploaded_sample[i].sample_id,
                      " can fetch enough molecuses in uploaded sample", file=sys.stderr)

                return self.uploaded_sample[i].sample_id

        print("Debug: No sample can fetch enough molecuses in uploaded sample", file=sys.stderr)
        return -1

    def get_enough_molecules_in_uploaded_sample(self, humanRobot):
        for i in range(len(self.uploaded_sample)):
            if self.uploaded_sample[i].cost_a <= (humanRobot.storage_a + humanRobot.expertise_a) \
                    and self.uploaded_sample[i].cost_b <= (humanRobot.storage_b + humanRobot.expertise_b) \
                    and self.uploaded_sample[i].cost_c <= (humanRobot.storage_c + humanRobot.expertise_c) \
                    and self.uploaded_sample[i].cost_d <= (humanRobot.storage_d + humanRobot.expertise_d) \
                    and self.uploaded_sample[i].cost_e <= (humanRobot.storage_e + humanRobot.expertise_e) \
                    and self.uploaded_sample[i].has_been_diagnosed() == True:
                print("Debug: find sample id", self.uploaded_sample[i].sample_id,
                      " already has enough molecuses in uploaded sample", file=sys.stderr)
                return self.uploaded_sample[i]

        print("Debug: No sample can has enough molecuses in uploaded sample", file=sys.stderr)
        return None


class Robot:
    MAX_CARRIED_MOLECULES_NUM = 10
    MAX_CARRIED_SAMPLE_NUM = 3

    TYPE_AI = 0
    TYPE_HUMAN = 1

    def __init__(self, game, robot_type):
        self.game = game
        self.robot_type = robot_type
        self.previous_target = ''
        self.current_target = 'START_POS'
        self.carrying_sample = []

        self.pre_storage_a = 0
        self.pre_storage_b = 0
        self.pre_storage_c = 0
        self.pre_storage_d = 0
        self.pre_storage_e = 0
        self.storage_a = 0
        self.storage_b = 0
        self.storage_c = 0
        self.storage_d = 0
        self.storage_e = 0
        self.detect_2_storage_a_spent = False
        self.detect_2_storage_b_spent = False
        self.detect_2_storage_c_spent = False
        self.detect_2_storage_d_spent = False
        self.detect_2_storage_e_spent = False

        self.expertise_a = 0
        self.expertise_b = 0
        self.expertise_c = 0
        self.expertise_d = 0
        self.expertise_e = 0

    def set_previous_target(self, previous_target):
        self.previous_target = previous_target

    def set_current_target(self, target):
        self.current_target = target

    def set_eta(self, eta):
        self.eta = eta

    def set_score(self, score):
        self.score = score

    def set_storage_a(self, storage_a):
        self.pre_storage_a = self.storage_a
        self.storage_a = storage_a

        if self.pre_storage_a - self.storage_a >= 2:
            self.detect_2_storage_a_spent = True

    def set_storage_b(self, storage_b):
        self.pre_storage_b = self.storage_b
        self.storage_b = storage_b

        if self.pre_storage_b - self.storage_b >= 2:
            self.detect_2_storage_b_spent = True

    def set_storage_c(self, storage_c):
        self.pre_storage_c = self.storage_c
        self.storage_c = storage_c

        if self.pre_storage_c - self.storage_c >= 2:
            self.detect_2_storage_c_spent = True

    def set_storage_d(self, storage_d):
        self.pre_storage_d = self.storage_d
        self.storage_d = storage_d

        if self.pre_storage_d - self.storage_d >= 2:
            self.detect_2_storage_d_spent = True

    def set_storage_e(self, storage_e):
        self.pre_storage_e = self.storage_e
        self.storage_e = storage_e

        if self.pre_storage_e - self.storage_e >= 2:
            self.detect_2_storage_e_spent = True

    def check_2_storage_spent(self, storage_type):
        if self.detect_2_storage_a_spent == True and storage_type == 'A':
            return True
        if self.detect_2_storage_b_spent == True and storage_type == 'B':
            return True
        if self.detect_2_storage_c_spent == True and storage_type == 'C':
            return True
        if self.detect_2_storage_d_spent == True and storage_type == 'D':
            return True
        if self.detect_2_storage_e_spent == True and storage_type == 'E':
            return True

        return False

    def get_used_storage(self):
        return self.storage_a + self.storage_b + self.storage_c + self.storage_d + self.storage_e

    def get_unused_storage(self):
        return 10 - (self.storage_a + self.storage_b + self.storage_c + self.storage_d + self.storage_e)

    def is_storage_full(self):
        return self.get_used_storage() >= self.MAX_CARRIED_MOLECULES_NUM

    def is_storage_empty(self):
        return self.get_used_storage() == 0

    def set_expertise_a(self, expertise_a):
        self.expertise_a = expertise_a

    def set_expertise_b(self, expertise_b):
        self.expertise_b = expertise_b

    def set_expertise_c(self, expertise_c):
        self.expertise_c = expertise_c

    def set_expertise_d(self, expertise_d):
        self.expertise_d = expertise_d

    def set_expertise_e(self, expertise_e):
        self.expertise_e = expertise_e

    def get_total_expertise(self):
        return self.expertise_a + self.expertise_b + self.expertise_c + self.expertise_d + self.expertise_e

    def set_rank(self, rank):
        self.rank = rank

    def add_carrying_sample(self, sample):
        for i in range(len(self.carrying_sample)):
            if sample.sample_id == self.carrying_sample[i].sample_id:
                self.carrying_sample.remove(self.carrying_sample[i])
                break

        for i in range(len(self.carrying_sample)):
            if sample.total_cost < self.carrying_sample[i].total_cost:
                self.carrying_sample.insert(i, sample)
                print("Debug: insert sample id", sample.sample_id, "at ", i, " in carrying sample", file=sys.stderr)
                return

        print("Debug: append sample id", sample.sample_id, "in carrying sample", file=sys.stderr)
        self.carrying_sample.append(sample)

    def is_carrying_sample_full(self):
        return len(self.carrying_sample) == self.MAX_CARRIED_SAMPLE_NUM

    def is_carrying_sample_empty(self):
        return len(self.carrying_sample) == 0

    def get_undiagnosed_sample_id(self):
        for i in range(len(self.carrying_sample)):
            if self.carrying_sample[i].has_been_diagnosed() == False:
                print("Debug: find an undiagnosed sample id", self.carrying_sample[i].sample_id, " in carrying sample",
                      file=sys.stderr)
                return self.carrying_sample[i].sample_id

        print("Debug: there is no undiagnosed sample in carrying sample", file=sys.stderr)
        return -1

    def get_being_uploaded_sample_id(self):
        for i in range(len(self.carrying_sample)):
            if myRobot.carrying_sample[i].shouldBeUploaded(self) == True:
                print("Debug: find an being uploaded sample id", self.carrying_sample[i].sample_id,
                      " in carrying sample", file=sys.stderr)
                return myRobot.carrying_sample[i].sample_id

        print("Debug: there is no being uploaded sample in carrying sample", file=sys.stderr)
        return -1

    def getSample(self, sample_id):
        for i in range(len(self.carrying_sample)):
            if sample_id == self.carrying_sample[i].sample_id:
                return self.carrying_sample[i]

        return None

    def deleteSample(self, sample_id):
        for i in range(len(self.carrying_sample)):
            if sample_id == self.carrying_sample[i].sample_id:
                self.carrying_sample.remove(self.carrying_sample[i])
                print("Debug: sample id", sample_id, " has been deleted from carrying sample", file=sys.stderr)
                return

    def markSampleNeedToBeDeleted(self, sample_id):
        for i in range(len(self.carrying_sample)):
            if sample_id == self.carrying_sample[i].sample_id:
                self.carrying_sample[i].mark_sample_to_be_deleted()
                print("Debug: sample id", sample_id, " mark as need to be deleted", file=sys.stderr)
                return

    def cleanUp(self):
        self.set_previous_target(self.current_target)

        self.detect_2_storage_a_spent = False
        self.detect_2_storage_b_spent = False
        self.detect_2_storage_c_spent = False
        self.detect_2_storage_d_spent = False
        self.detect_2_storage_e_spent = False

        max_range = len(self.carrying_sample)
        i = 0
        while i < max_range:
            if self.carrying_sample[i].has_been_marked_as_deleted() == True:
                print("Debug: sample id", self.carrying_sample[i].sample_id, " has been deleted from carrying sample",
                      file=sys.stderr)

                self.carrying_sample.remove(self.carrying_sample[i])
                i = 0
                max_range = len(self.carrying_sample)

            i = i + 1

    def getSampleIdWhichCanFetchEnoughMoleculesFromModule(self, aiRobot):
        for i in range(len(self.carrying_sample)):
            molecuse_a_enough = True
            molecuse_b_enough = True
            molecuse_c_enough = True
            molecuse_d_enough = True
            molecuse_e_enough = True

            if self.carrying_sample[i].cost_a > 0 \
                    and (self.carrying_sample[i].cost_a - self.storage_a - self.expertise_a) > 0 \
                    and (self.game.get_max_molecuse_a() - aiRobot.storage_a - self.storage_a) <= 0:
                needed_molecue_a = self.carrying_sample[i].cost_a - self.storage_a - self.expertise_a
                print("Debug: molecuse A is not enough for ", self.carrying_sample[i].sample_id, "need ",
                      needed_molecue_a, file=sys.stderr)
                molecuse_a_enough = False

            if self.carrying_sample[i].cost_b > 0 \
                    and (self.carrying_sample[i].cost_b - self.storage_b - self.expertise_b) > 0 \
                    and (self.game.get_max_molecuse_b() - aiRobot.storage_b - self.storage_b) <= 0:
                needed_molecue_b = self.carrying_sample[i].cost_b - self.storage_b - self.expertise_b
                print("Debug: molecuse B is not enough for ", self.carrying_sample[i].sample_id, "need ",
                      needed_molecue_b, file=sys.stderr)
                molecuse_b_enough = False

            if self.carrying_sample[i].cost_c > 0 \
                    and (self.carrying_sample[i].cost_c - self.storage_c - self.expertise_c) > 0 \
                    and (self.game.get_max_molecuse_c() - aiRobot.storage_c - self.storage_c) <= 0:
                needed_molecue_c = self.carrying_sample[i].cost_c - self.storage_c - self.expertise_c
                print("Debug: molecuse C is not enough for ", self.carrying_sample[i].sample_id, "need ",
                      needed_molecue_c, file=sys.stderr)
                molecuse_c_enough = False

            if self.carrying_sample[i].cost_d > 0 \
                    and (self.carrying_sample[i].cost_d - self.storage_d - self.expertise_d) > 0 \
                    and (self.game.get_max_molecuse_d() - aiRobot.storage_d - self.storage_d) <= 0:
                needed_molecue_d = self.carrying_sample[i].cost_d - self.storage_d - self.expertise_d
                print("Debug: molecuse D is not enough for ", self.carrying_sample[i].sample_id, "need ",
                      needed_molecue_d, file=sys.stderr)
                molecuse_d_enough = False

            if self.carrying_sample[i].cost_e > 0 \
                    and (self.carrying_sample[i].cost_e - self.storage_e - self.expertise_e) > 0 \
                    and (self.game.get_max_molecuse_e() - aiRobot.storage_e - self.storage_e) <= 0:
                needed_molecue_e = self.carrying_sample[i].cost_e - self.storage_e - self.expertise_e
                print("Debug: molecuse D is not enough for ", self.carrying_sample[i].sample_id, "need ",
                      needed_molecue_e, file=sys.stderr)
                molecuse_e_enough = False

            if self.carrying_sample[i].shouldBeUploaded(self) == False \
                    and molecuse_a_enough == True \
                    and molecuse_b_enough == True \
                    and molecuse_c_enough == True \
                    and molecuse_d_enough == True \
                    and molecuse_e_enough == True:
                print("Debug: find sample id", self.carrying_sample[i].sample_id, " can fetch enough molecuses",
                      file=sys.stderr)

                return self.carrying_sample[i].sample_id

        print("Debug: No sample can fetch enough molecuses", file=sys.stderr)
        return -1

    def getNotEnoughMolecuseType(self, aiRobot):
        for i in range(len(self.carrying_sample)):
            molecuse_a_enough = True
            molecuse_b_enough = True
            molecuse_c_enough = True
            molecuse_d_enough = True
            molecuse_e_enough = True

            if self.carrying_sample[i].cost_a > 0 \
                    and (self.carrying_sample[i].cost_a - self.storage_a - self.expertise_a) > 0 \
                    and (self.game.get_max_molecuse_a() - aiRobot.storage_a - self.storage_a) <= 0:
                print("Debug: molecuse A is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return 'A'

            if self.carrying_sample[i].cost_b > 0 \
                    and (self.carrying_sample[i].cost_b - self.storage_b - self.expertise_b) > 0 \
                    and (self.game.get_max_molecuse_b() - aiRobot.storage_b - self.storage_b) <= 0:
                print("Debug: molecuse B is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return 'B'

            if self.carrying_sample[i].cost_c > 0 \
                    and (self.carrying_sample[i].cost_c - self.storage_c - self.expertise_c) > 0 \
                    and (self.game.get_max_molecuse_c() - aiRobot.storage_c - self.storage_c) <= 0:
                print("Debug: molecuse C is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return 'C'

            if self.carrying_sample[i].cost_d > 0 \
                    and (self.carrying_sample[i].cost_d - self.storage_d - self.expertise_d) > 0 \
                    and (self.game.get_max_molecuse_d() - aiRobot.storage_d - self.storage_d) <= 0:
                print("Debug: molecuse D is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return 'D'

            if self.carrying_sample[i].cost_e > 0 \
                    and (self.carrying_sample[i].cost_e - self.storage_e - self.expertise_e) > 0 \
                    and (self.game.get_max_molecuse_e() - aiRobot.storage_e - self.storage_e) <= 0:
                print("Debug: molecuse D is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return 'E'

        print("Debug: No molecuse is empty in module", file=sys.stderr)
        return ''

    def getSampleIdWhichCanNotFetchEnoughMoleculesFromModule(self, aiRobot):
        for i in range(len(self.carrying_sample)):
            needed_molecue_a = 0
            needed_molecue_b = 0
            needed_molecue_c = 0
            needed_molecue_d = 0
            needed_molecue_e = 0

            if self.carrying_sample[i].cost_a > 0 \
                    and (self.carrying_sample[i].cost_a - self.storage_a - self.expertise_a) > 0 \
                    and (self.game.get_max_molecuse_a() - aiRobot.storage_a - self.storage_a) <= 0:
                print("Debug: molecuse A is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return self.carrying_sample[i].sample_id

            if self.carrying_sample[i].cost_b > 0 \
                    and (self.carrying_sample[i].cost_b - self.storage_b - self.expertise_b) > 0 \
                    and (self.game.get_max_molecuse_b() - aiRobot.storage_b - self.storage_b) <= 0:
                print("Debug: molecuse B is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return self.carrying_sample[i].sample_id

            if self.carrying_sample[i].cost_c > 0 \
                    and (self.carrying_sample[i].cost_c - self.storage_c - self.expertise_c) > 0 \
                    and (self.game.get_max_molecuse_c() - aiRobot.storage_c - self.storage_c) <= 0:
                print("Debug: molecuse C is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return self.carrying_sample[i].sample_id

            if self.carrying_sample[i].cost_d > 0 \
                    and (self.carrying_sample[i].cost_d - self.storage_d - self.expertise_d) > 0 \
                    and (self.game.get_max_molecuse_d() - aiRobot.storage_d - self.storage_d) <= 0:
                print("Debug: molecuse D is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return self.carrying_sample[i].sample_id

            if self.carrying_sample[i].cost_e > 0 \
                    and (self.carrying_sample[i].cost_e - self.storage_e - self.expertise_e) > 0 \
                    and (self.game.get_max_molecuse_e() - aiRobot.storage_e - self.storage_e) <= 0:
                print("Debug: molecuse E is not enough for ", self.carrying_sample[i].sample_id, file=sys.stderr)
                return self.carrying_sample[i].sample_id

            if self.carrying_sample[i].cost_a - self.storage_a - self.expertise_a > 0:
                needed_molecue_a = self.carrying_sample[i].cost_a - self.storage_a - self.expertise_a
            if self.carrying_sample[i].cost_b - self.storage_b - self.expertise_b > 0:
                needed_molecue_b = self.carrying_sample[i].cost_b - self.storage_b - self.expertise_b
            if self.carrying_sample[i].cost_c - self.storage_c - self.expertise_c > 0:
                needed_molecue_c = self.carrying_sample[i].cost_c - self.storage_c - self.expertise_c
            if self.carrying_sample[i].cost_d - self.storage_d - self.expertise_d > 0:
                needed_molecue_d = self.carrying_sample[i].cost_d - self.storage_d - self.expertise_d
            if self.carrying_sample[i].cost_e - self.storage_e - self.expertise_e > 0:
                needed_molecue_e = self.carrying_sample[i].cost_e - self.storage_e - self.expertise_e

            if (needed_molecue_a + needed_molecue_b + needed_molecue_c + needed_molecue_d + needed_molecue_e) \
                    > self.get_unused_storage() \
                    and self.carrying_sample[i].shouldBeUploaded(self) == False:
                return self.carrying_sample[i].sample_id

        if self.is_carrying_sample_empty() == True:
            print("Debug: carrying sample is empty", file=sys.stderr)
        else:
            print("Debug: all sample can fetch enough molecuses", file=sys.stderr)
        return -1

    def has_enough_molecules_for_sample(self):
        for i in range(len(self.carrying_sample)):
            if self.carrying_sample[i].cost_a <= (self.storage_a + self.expertise_a) \
                    and self.carrying_sample[i].cost_b <= (self.storage_b + self.expertise_b) \
                    and self.carrying_sample[i].cost_c <= (self.storage_c + self.expertise_c) \
                    and self.carrying_sample[i].cost_d <= (self.storage_d + self.expertise_d) \
                    and self.carrying_sample[i].cost_e <= (self.storage_e + self.expertise_e) \
                    and self.carrying_sample[i].has_been_diagnosed() == True:
                return True

        return False

    def get_enough_molecules_sample_id(self):
        for i in range(len(self.carrying_sample)):
            if self.carrying_sample[i].cost_a <= (self.storage_a + self.expertise_a) \
                    and self.carrying_sample[i].cost_b <= (self.storage_b + self.expertise_b) \
                    and self.carrying_sample[i].cost_c <= (self.storage_c + self.expertise_c) \
                    and self.carrying_sample[i].cost_d <= (self.storage_d + self.expertise_d) \
                    and self.carrying_sample[i].cost_e <= (self.storage_e + self.expertise_e) \
                    and self.carrying_sample[i].has_been_diagnosed() == True:
                return self.carrying_sample[i].sample_id

        return -1


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

        print("Debug: new a sample, id", self.sample_id, \
              ",expertise_gain", self.expertise_gain, \
              ",total cost", self.total_cost, \
              ",health", self.health, \
              ",cost_a ", self.cost_a, \
              ",cost_b ", self.cost_b, \
              ",cost_c ", self.cost_c, \
              ",cost_d ", self.cost_d, \
              ",cost_e ", self.cost_e, \
              file=sys.stderr)

    def updateSample(self, sample):
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

    def shouldBeUploaded(self, robot):
        if self.has_been_diagnosed() == True:
            if self.cost_a - robot.expertise_a > self.game.get_max_molecuse_a() \
                    or self.cost_b - robot.expertise_b > self.game.get_max_molecuse_b() \
                    or self.cost_c - robot.expertise_c > self.game.get_max_molecuse_c() \
                    or self.cost_d - robot.expertise_d > self.game.get_max_molecuse_d() \
                    or self.cost_e - robot.expertise_e > self.game.get_max_molecuse_e():
                return True

            molecuse_a = 0
            molecuse_b = 0
            molecuse_c = 0
            molecuse_d = 0
            molecuse_e = 0
            if self.cost_a - robot.expertise_a > 0:
                molecuse_a = self.cost_a - robot.expertise_a
            if self.cost_b - robot.expertise_b > 0:
                molecuse_b = self.cost_b - robot.expertise_b
            if self.cost_c - robot.expertise_c > 0:
                molecuse_c = self.cost_c - robot.expertise_c
            if self.cost_d - robot.expertise_d > 0:
                molecuse_d = self.cost_d - robot.expertise_d
            if self.cost_e - robot.expertise_e > 0:
                molecuse_e = self.cost_e - robot.expertise_e
            if molecuse_a + molecuse_b + molecuse_c + molecuse_d + molecuse_e > 10:
                return True

        return False


game = Game()
myRobot = Robot(game, Robot.TYPE_HUMAN)
aiRobot = Robot(game, Robot.TYPE_AI)


def steps(from_position, to_position):
    if (from_position == 'START_POS' and to_position == 'SAMPLES'):
        return 2
    elif (from_position == 'START_POS' and to_position == 'DIAGNOSIS'):
        return 2
    elif (from_position == 'START_POS' and to_position == 'MOLECULES'):
        return 2
    elif (from_position == 'START_POS' and to_position == 'LABORATORY'):
        return 2
    elif (from_position == 'SAMPLES' and to_position == 'DIAGNOSIS'):
        return 3
    elif (from_position == 'SAMPLES' and to_position == 'MOLECULES'):
        return 3
    elif (from_position == 'SAMPLES' and to_position == 'LABORATORY'):
        return 3
    elif (from_position == 'DIAGNOSIS' and to_position == 'SAMPLES'):
        return 3
    elif (from_position == 'DIAGNOSIS' and to_position == 'MOLECULES'):
        return 3
    elif (from_position == 'DIAGNOSIS' and to_position == 'LABORATORY'):
        return 4
    elif (from_position == 'MOLECULES' and to_position == 'SAMPLES'):
        return 3
    elif (from_position == 'MOLECULES' and to_position == 'DIAGNOSIS'):
        return 3
    elif (from_position == 'MOLECULES' and to_position == 'LABORATORY'):
        return 3
    elif (from_position == 'LABORATORY' and to_position == 'SAMPLES'):
        return 3
    elif (from_position == 'LABORATORY' and to_position == 'DIAGNOSIS'):
        return 4
    elif (from_position == 'LABORATORY' and to_position == 'MOLECULES'):
        return 3


def checkAiRobotMolecuseSpent():
    global myRobot
    global aiRobot


def shouldJumpToNextTurn():
    global myRobot
    global aiRobot

    if myRobot.eta == 0:
        return False
    else:
        print("Debug: myRobot should do nothing in this turn", file=sys.stderr)
        print("go go go")
        return True


def fetch_molecules(sample_id):
    global myRobot
    global aiRobot
    global game

    print("DEBUG: try to get molecules for sample_id=", sample_id, file=sys.stderr)

    for i in range(len(myRobot.carrying_sample)):
        if myRobot.carrying_sample[i].sample_id == sample_id:
            if ((myRobot.carrying_sample[i].cost_a - myRobot.storage_a - myRobot.expertise_a) > 0 and (
                    game.get_max_molecuse_a() - aiRobot.storage_a - myRobot.storage_a) > 0):
                print("DEBUG: myRobot get molecules A for sample_id=", sample_id, file=sys.stderr)
                print("CONNECT A")
                return
            elif ((myRobot.carrying_sample[i].cost_b - myRobot.storage_b - myRobot.expertise_b) > 0 and (
                    game.get_max_molecuse_b() - aiRobot.storage_b - myRobot.storage_b) > 0):
                print("DEBUG: myRobot get molecules B for sample_id=", sample_id, file=sys.stderr)
                print("CONNECT B")
                return
            elif ((myRobot.carrying_sample[i].cost_c - myRobot.storage_c - myRobot.expertise_c) > 0 and (
                    game.get_max_molecuse_c() - aiRobot.storage_c - myRobot.storage_c) > 0):
                print("DEBUG: myRobot get molecules C for sample_id=", sample_id, file=sys.stderr)
                print("CONNECT C")
                return
            elif ((myRobot.carrying_sample[i].cost_d - myRobot.storage_d - myRobot.expertise_d) > 0 and (
                    game.get_max_molecuse_d() - aiRobot.storage_d - myRobot.storage_d) > 0):
                print("DEBUG: myRobot get molecules D for sample_id=", sample_id, file=sys.stderr)
                print("CONNECT D")
                return
            elif ((myRobot.carrying_sample[i].cost_e - myRobot.storage_e - myRobot.expertise_e) > 0 and (
                    game.get_max_molecuse_e() - aiRobot.storage_e - myRobot.storage_e) > 0):
                print("DEBUG: myRobot get molecules E for sample_id=", sample_id, file=sys.stderr)
                print("CONNECT E")
                return

    print("DEBUG: NO more molecules for sample_id=", sample_id, " ,shoule wait", file=sys.stderr)
    print("WAIT")


def generate_rank():
    global myRobot
    global aiRobot
    global game

    game.rank_count = game.rank_count + 1

    if game.rank_count < 6:
        return 1
    elif game.rank_count >= 6 and game.rank_count < 10:
        return 2
    elif myRobot.get_used_storage() >= 4:
        if len(myRobot.carrying_sample) == 0:
            return 1
        elif len(myRobot.carrying_sample) == 1:
            if myRobot.get_total_expertise() >= 4:
                return 1
            else:
                return 3
        else:
            return 2
    elif myRobot.get_used_storage() >= 2:
        if len(myRobot.carrying_sample) >= 1:
            return 1
        elif len(myRobot.carrying_sample) == 1:
            return 2
        else:
            return 3
    elif myRobot.get_total_expertise() >= 10:
        if len(myRobot.carrying_sample) == 0:
            return 3
        elif len(myRobot.carrying_sample) == 1:
            return 3
        else:
            return 3
    elif myRobot.get_total_expertise() >= 10:
        return 3

    elif myRobot.get_total_expertise() >= 6:
        return 2
    return 1


def cleanUp():
    global myRobot
    global aiRobot
    global game

    myRobot.cleanUp()
    aiRobot.cleanUp()
    game.cleanUp()


##############################################################################################
def go_to_samples():
    global myRobot
    global aiRobot

    if myRobot.current_target == 'START_POS':
        # game start
        print("DEBUG: my robot go to SAMPLES", file=sys.stderr)
        print("GOTO SAMPLES")
    elif (myRobot.previous_target == 'LABORATORY' and myRobot.current_target == 'LABORATORY'):
        if myRobot.is_carrying_sample_empty() == True:
            print("DEBUG: my robot go to SAMPLES due to carrying sample empty", file=sys.stderr)
            print("GOTO SAMPLES")
        elif myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot) == -1:
            print("DEBUG: my robot go to SAMPLES dut to NO sample can fetch enouth molecuse", file=sys.stderr)
            print("GOTO SAMPLES")
    elif (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'DIAGNOSIS'):
        canFetchEnoughMolecuseSample = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)
        canNotnotEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanNotFetchEnoughMoleculesFromModule(aiRobot)
        canFetchEnoughMoleculesUploadedSampleId = game.getSampleIdWhichCanFetchEnoughMoleculesFromModuleInUploadedSample(
            myRobot, aiRobot)
        enoughMolecuseUploadedSample = game.get_enough_molecules_in_uploaded_sample(myRobot)

        if myRobot.is_carrying_sample_empty() == True \
                and canFetchEnoughMoleculesUploadedSampleId == -1 \
                and enoughMolecuseUploadedSample is None:
            print("DEBUG: my robot go to SAMPLES due to carrying sample empty and NO sample can be downloaded",
                  file=sys.stderr)
            print("GOTO SAMPLES")
        elif myRobot.is_carrying_sample_empty() == True \
                and canFetchEnoughMoleculesUploadedSampleId != -1 \
                and myRobot.is_storage_full() == True \
                and enoughMolecuseUploadedSample is None:
            print(
                "DEBUG: my robot go to SAMPLES due to storage full and carrying sample empty and NO sample to download",
                file=sys.stderr)
            print("GOTO SAMPLES")


    elif (myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == False:
            canFetchEnoughMolecuseSample = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)
            if canFetchEnoughMolecuseSample == -1:
                if (aiRobot.current_target != 'MOLECULES' and aiRobot.current_target != 'LABORATORY') \
                        and myRobot.is_carrying_sample_full() == False:
                    print("DEBUG: my robot go to SAMPLES due to no enough molecuse", file=sys.stderr)
                    print("GOTO SAMPLES")
            else:
                if myRobot.is_storage_full() == True and myRobot.is_carrying_sample_full() == False:
                    print("DEBUG: my robot go to SAMPLES due to storage is full", file=sys.stderr)
                    print("GOTO SAMPLES")


def go_to_diagnosis():
    global myRobot
    global aiRobot

    if (myRobot.previous_target == 'SAMPLES' and myRobot.current_target == 'SAMPLES'):
        if myRobot.is_carrying_sample_full() == True:
            print("DEBUG: my robot go to DIAGNOSIS", file=sys.stderr)
            print("GOTO DIAGNOSIS")
    elif (myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == False:
            if myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot) == -1:
                if aiRobot.current_target != 'MOLECULES' \
                        and aiRobot.current_target != 'LABORATORY' \
                        and myRobot.is_carrying_sample_full() == True:
                    print("DEBUG: my robot go to DIAGNOSIS due to no enough molecuse", file=sys.stderr)
                    print("GOTO DIAGNOSIS")
            else:
                if myRobot.is_storage_full() == True and myRobot.is_carrying_sample_full() == True:
                    print("DEBUG: my robot go to DIAGNOSIS due to storage is full", file=sys.stderr)
                    print("GOTO DIAGNOSIS")


def go_to_molecules():
    global myRobot
    global aiRobot

    if (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'DIAGNOSIS'):
        canNotFetchEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanNotFetchEnoughMoleculesFromModule(aiRobot)
        canFetchEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)
        canFetchEnoughMoleculesUploadedSampleId = \
            game.getSampleIdWhichCanFetchEnoughMoleculesFromModuleInUploadedSample(myRobot, aiRobot)
        enoughMolecuseUploadedSample = game.get_enough_molecules_in_uploaded_sample(myRobot)

        if myRobot.get_undiagnosed_sample_id() == -1 \
                and myRobot.get_being_uploaded_sample_id() == -1 \
                and myRobot.has_enough_molecules_for_sample() == False \
                and myRobot.is_storage_full() == False:

            if myRobot.is_carrying_sample_full() == False:
                if enoughMolecuseUploadedSample is None \
                        and canFetchEnoughMolecuseSampleId != -1:
                    print(
                        "DEBUG: my robot go to MOLECULES due to due to one of carrying sample can fetch molecuse and enoughMolecuseUploadedSample is None",
                        file=sys.stderr)
                    print("GOTO MOLECULES")
            elif myRobot.is_carrying_sample_full() == True:
                if canFetchEnoughMolecuseSampleId != -1:
                    print("DEBUG: my robot go to MOLECULES due to one of carrying sample can fetch molecuse",
                          file=sys.stderr)
                    print("GOTO MOLECULES")

    elif myRobot.previous_target == 'LABORATORY' and myRobot.current_target == 'LABORATORY':
        canNotFetchEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanNotFetchEnoughMoleculesFromModule(aiRobot)
        canFetchEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)
        canFetchEnoughMoleculesSampleId = \
            game.getSampleIdWhichCanFetchEnoughMoleculesFromModuleInUploadedSample(myRobot, aiRobot)
        enoughMolecuseUploadedSample = game.get_enough_molecules_in_uploaded_sample(myRobot)

        if canFetchEnoughMolecuseSampleId != -1 \
                and myRobot.has_enough_molecules_for_sample() == False:
            print("DEBUG: my robot go to MOLECULES due to sample can fetch molecuse and no sample got enough molecuses",
                  file=sys.stderr)
            print("GOTO MOLECULES")


def go_to_laboratory():
    global myRobot
    global aiRobot

    if (myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == True:
            print("DEBUG: my robot go to LABORATORY", file=sys.stderr)
            print("GOTO LABORATORY")
    elif (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == True:
            print("DEBUG: my robot go to LABORATORY", file=sys.stderr)
            print("GOTO LABORATORY")
    elif (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'DIAGNOSIS'):
        if myRobot.get_undiagnosed_sample_id() == -1 \
                and myRobot.get_being_uploaded_sample_id() == -1 \
                and myRobot.has_enough_molecules_for_sample() == True:
            print("DEBUG: my robot go to LABORATORY", file=sys.stderr)
            print("GOTO LABORATORY")


#################################################################################################
def get_rank():
    global myRobot
    global aiRobot

    rank = generate_rank()

    if (myRobot.previous_target == 'START_POS'):
        if myRobot.is_carrying_sample_full() == False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    if (myRobot.previous_target == 'SAMPLES' and myRobot.current_target == 'SAMPLES'):
        if myRobot.is_carrying_sample_full() == False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif (myRobot.previous_target == 'LABORATORY' and myRobot.current_target == 'SAMPLES'):
        if myRobot.is_carrying_sample_full() == False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'SAMPLES'):
        if myRobot.is_carrying_sample_full() == False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)
    elif (myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'SAMPLES'):
        if myRobot.is_carrying_sample_full() == False:
            print("DEBUG: my robot get rank", rank, file=sys.stderr)
            print("CONNECT ", rank)


def get_diagnose():
    global myRobot
    global aiRobot

    if (myRobot.previous_target == 'SAMPLES' and myRobot.current_target == 'DIAGNOSIS'):
        undiagnosed_sample_id = myRobot.get_undiagnosed_sample_id()
        if undiagnosed_sample_id > -1:
            print("DEBUG: my robot diagnose sample id", undiagnosed_sample_id, file=sys.stderr)
            print("CONNECT ", undiagnosed_sample_id)
    elif myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'DIAGNOSIS':
        undiagnosed_sample_id = myRobot.get_undiagnosed_sample_id()
        if undiagnosed_sample_id > -1:
            print("DEBUG: my robot diagnose sample id", undiagnosed_sample_id, file=sys.stderr)
            print("CONNECT ", undiagnosed_sample_id)


def upload_sample():
    global myRobot
    global aiRobot
    global game

    if (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'DIAGNOSIS'):

        if myRobot.get_undiagnosed_sample_id() == -1:
            uploaded_sample_id = myRobot.get_being_uploaded_sample_id()
            if uploaded_sample_id > -1:
                print("DEBUG: my robot upload sample id", uploaded_sample_id, " due to its cost", file=sys.stderr)
                myRobot.markSampleNeedToBeDeleted(uploaded_sample_id)
                print("CONNECT ", uploaded_sample_id)
            else:
                canNotFetchEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanNotFetchEnoughMoleculesFromModule(
                    aiRobot)
                canFetchEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)
                canFetchEnoughMoleculesUploadedSampleId = game.getSampleIdWhichCanFetchEnoughMoleculesFromModuleInUploadedSample(
                    myRobot, aiRobot)
                enoughMolecuseUploadedSample = game.get_enough_molecules_in_uploaded_sample(myRobot)

                if myRobot.has_enough_molecules_for_sample() == False \
                        and enoughMolecuseUploadedSample is not None \
                        and canFetchEnoughMolecuseSampleId == -1 \
                        and myRobot.is_carrying_sample_full() == False:
                    print("DEBUG: my robot download ", enoughMolecuseUploadedSample.sample_id,
                          " which has been uploaded before already have enough molecuses", file=sys.stderr)
                    print("CONNECT ", enoughMolecuseUploadedSample.sample_id)  # download sample
                elif myRobot.has_enough_molecules_for_sample() == False \
                        and canFetchEnoughMoleculesUploadedSampleId != -1 \
                        and myRobot.is_storage_full() == False \
                        and canFetchEnoughMolecuseSampleId == -1 \
                        and myRobot.is_carrying_sample_full() == False:
                    print("DEBUG: my robot download ", canFetchEnoughMoleculesUploadedSampleId,
                          " which has been uploaded before", file=sys.stderr)
                    print("CONNECT ", canFetchEnoughMoleculesUploadedSampleId)  # download sample
                elif canFetchEnoughMolecuseSampleId == -1 \
                        and canNotFetchEnoughMolecuseSampleId != -1 \
                        and myRobot.has_enough_molecules_for_sample() == False:
                    if (aiRobot.current_target == 'MOLECULES' \
                            or aiRobot.current_target == 'LABORATORY') \
                         and myRobot.is_storage_full() == False:
                        print("DEBUG: ai robot will spend molecuse", file=sys.stderr)
                        print("DEBUG: my robot WAIT for molecuse", file=sys.stderr)
                        print("WAIT")
                    else:
                        print("DEBUG: my robot upload sample id", canNotFetchEnoughMolecuseSampleId,
                              " WhichCanNotFetchEnoughMoleculesFromModule", file=sys.stderr)
                        myRobot.markSampleNeedToBeDeleted(canNotFetchEnoughMolecuseSampleId)
                        print("CONNECT ", canNotFetchEnoughMolecuseSampleId)
                elif myRobot.is_storage_full() == True and myRobot.has_enough_molecules_for_sample() == False:
                    if canFetchEnoughMolecuseSampleId != -1:
                        print("DEBUG: my robot upload sample id", canFetchEnoughMolecuseSampleId,
                              " due to storage is full",
                              file=sys.stderr)
                        myRobot.markSampleNeedToBeDeleted(canFetchEnoughMolecuseSampleId)
                        print("CONNECT ", canFetchEnoughMolecuseSampleId)

    elif (myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'DIAGNOSIS'):
        if myRobot.get_undiagnosed_sample_id() == -1:
            notEnoughMolecuseSampleId = myRobot.getSampleIdWhichCanNotFetchEnoughMoleculesFromModule(aiRobot)
            enoughMolecuseSampleId = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)
            canFetchEnoughMoleculesUploadedSampleId = game.getSampleIdWhichCanFetchEnoughMoleculesFromModuleInUploadedSample(
                myRobot, aiRobot)
            enoughMolecuseUploadedSample = game.get_enough_molecules_in_uploaded_sample(myRobot)

            if myRobot.has_enough_molecules_for_sample() == False \
                    and enoughMolecuseUploadedSample is not None \
                    and myRobot.is_carrying_sample_full() == False:
                print("DEBUG: my robot download ", enoughMolecuseUploadedSample.sample_id,
                      " which has been uploaded before already have enough molecuses", file=sys.stderr)
                print("CONNECT ", enoughMolecuseUploadedSample.sample_id)  # download sample
            elif myRobot.has_enough_molecules_for_sample() == False \
                    and canFetchEnoughMoleculesUploadedSampleId != -1 \
                    and myRobot.is_storage_full() == False \
                    and myRobot.is_carrying_sample_full() == False:
                print("DEBUG: my robot download ", canFetchEnoughMoleculesUploadedSampleId,
                      " which has been uploaded before", file=sys.stderr)
                print("CONNECT ", canFetchEnoughMoleculesUploadedSampleId)  # download sample
            elif notEnoughMolecuseSampleId != -1 \
                    and myRobot.has_enough_molecules_for_sample() == False:
                if aiRobot.current_target == 'MOLECULES' or aiRobot.current_target == 'LABORATORY':
                    print("DEBUG: ai robot will spend molecuse", file=sys.stderr)
                    print("DEBUG: my robot WAIT for molecuse", file=sys.stderr)
                    print("WAIT")
                else:
                    print("DEBUG: my robot upload sample id", notEnoughMolecuseSampleId,
                          " WhichCanNotFetchEnoughMoleculesFromModule", file=sys.stderr)
                    myRobot.markSampleNeedToBeDeleted(notEnoughMolecuseSampleId)
                    print("CONNECT ", notEnoughMolecuseSampleId)
            elif myRobot.is_storage_full() == True and myRobot.has_enough_molecules_for_sample() == False:
                if enoughMolecuseSampleId != -1:
                    print("DEBUG: my robot upload sample id", enoughMolecuseSampleId, " due to storage is full",
                          file=sys.stderr)
                    myRobot.markSampleNeedToBeDeleted(enoughMolecuseSampleId)
                    print("CONNECT ", enoughMolecuseSampleId)


def get_molecules():
    global myRobot
    global aiRobot

    smapleIdWhichCanFetchEnoughMolecuse = myRobot.getSampleIdWhichCanFetchEnoughMoleculesFromModule(aiRobot)

    if (myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == False:
            if smapleIdWhichCanFetchEnoughMolecuse != -1:
                fetch_molecules(smapleIdWhichCanFetchEnoughMolecuse)
            else:
                print("DEBUG: my robot should wait due to not enough molecuse", file=sys.stderr)
                print("WAIT")
    elif (myRobot.previous_target == 'LABORATORY' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == False:
            if smapleIdWhichCanFetchEnoughMolecuse != -1:
                fetch_molecules(smapleIdWhichCanFetchEnoughMolecuse)
            else:
                print("DEBUG: my robot should wait due to not enough molecuse", file=sys.stderr)
                print("WAIT")
    elif (myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'MOLECULES'):
        if myRobot.has_enough_molecules_for_sample() == False:
            if smapleIdWhichCanFetchEnoughMolecuse != -1:
                if myRobot.is_storage_full() == False:
                    fetch_molecules(smapleIdWhichCanFetchEnoughMolecuse)
            else:
                if (aiRobot.current_target == 'MOLECULES' or aiRobot.current_target == 'LABORATORY'):
                    print("DEBUG: aiRobot will spend molecuse", file=sys.stderr)
                    print("DEBUG: my robot should wait due to not enough molecuse", file=sys.stderr)
                    print("WAIT")


def extract_medicine():
    global myRobot
    global aiRobot

    sample_id = myRobot.get_enough_molecules_sample_id()

    if myRobot.previous_target == 'MOLECULES' and myRobot.current_target == 'LABORATORY':
        print("DEBUG: my robot extract medicine for sample id", sample_id, file=sys.stderr)
        myRobot.markSampleNeedToBeDeleted(sample_id)
        print("CONNECT ", sample_id)
    elif myRobot.previous_target == 'DIAGNOSIS' and myRobot.current_target == 'LABORATORY':
        print("DEBUG: my robot extract medicine for sample id", sample_id, file=sys.stderr)
        myRobot.markSampleNeedToBeDeleted(sample_id)
        print("CONNECT ", sample_id)
    elif myRobot.previous_target == 'LABORATORY' and myRobot.current_target == 'LABORATORY':
        if sample_id != -1:
            print("DEBUG: my robot extract medicine for sample id", sample_id, file=sys.stderr)
            myRobot.markSampleNeedToBeDeleted(sample_id)
            print("CONNECT ", sample_id)


#############################################################################
project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]
    game.addScienceProject(ScienceProject(i, a, b, c, d, e))

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
            print("Debug: myRobot previous_target is ", myRobot.previous_target, \
                  ", current_target is ", myRobot.current_target, \
                  file=sys.stderr)
            print("Debug: myRobot eta is", eta, \
                  ", score is", score, \
                  file=sys.stderr)
            print("Debug: myRobot expertise_a is", expertise_a, \
                  ", expertise_b is", expertise_b, \
                  ", expertise_c is", expertise_c, \
                  ", expertise_d is", expertise_d, \
                  ", expertise_e is", expertise_e, \
                  file=sys.stderr)
            print("Debug: storage_a is", storage_a, \
                  ", storage_b is", storage_b, \
                  ", storage_c is", storage_c, \
                  ", storage_d is", storage_d, \
                  ", storage_e is", storage_e, \
                  file=sys.stderr)
            myRobot.set_current_target(target)
            myRobot.set_eta(eta)
            myRobot.set_score(score)
            myRobot.set_storage_a(storage_a)
            myRobot.set_storage_b(storage_b)
            myRobot.set_storage_c(storage_c)
            myRobot.set_storage_d(storage_d)
            myRobot.set_storage_e(storage_e)
            myRobot.set_expertise_a(expertise_a)
            myRobot.set_expertise_b(expertise_b)
            myRobot.set_expertise_c(expertise_c)
            myRobot.set_expertise_d(expertise_d)
            myRobot.set_expertise_e(expertise_e)
        elif i == 1:
            current_target = target
            aiRobot.set_current_target(target)
            aiRobot.set_eta(eta)
            aiRobot.set_score(score)
            aiRobot.set_storage_a(storage_a)
            aiRobot.set_storage_b(storage_b)
            aiRobot.set_storage_c(storage_c)
            aiRobot.set_storage_d(storage_d)
            aiRobot.set_storage_e(storage_e)
            aiRobot.set_expertise_a(expertise_a)
            aiRobot.set_expertise_b(expertise_b)
            aiRobot.set_expertise_c(expertise_c)
            aiRobot.set_expertise_d(expertise_d)
            aiRobot.set_expertise_e(expertise_e)
            print("Debug: aiRobot previous_target is ", aiRobot.previous_target, \
                  ", current_target is ", aiRobot.current_target, \
                  file=sys.stderr)
            print("Debug: aiRobot eta is", eta, \
                  ", score is", score, \
                  file=sys.stderr)
            print("Debug: aiRobot expertise_a is", expertise_a, \
                  ", expertise_b is", expertise_b, \
                  ", expertise_c is", expertise_c, \
                  ", expertise_d is", expertise_d, \
                  ", expertise_e is", expertise_e, \
                  file=sys.stderr)
            print("Debug: storage_a is", storage_a, \
                  ", storage_b is", storage_b, \
                  ", storage_c is", storage_c, \
                  ", storage_d is", storage_d, \
                  ", storage_e is", storage_e, \
                  file=sys.stderr)
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]

    sample_count = int(input())

    print("Debug: sample_count", sample_count, file=sys.stderr)

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
            myRobot.add_carrying_sample(
                Sample(game, sample_id, carried_by, health, rank, expertise_gain, total_cost, cost_a, cost_b, cost_c,
                       cost_d, cost_e))
        else:
            myRobot.deleteSample(sample_id)

        if carried_by == -1:
            game.add_uploaded_sample(
                Sample(game, sample_id, carried_by, health, rank, expertise_gain, total_cost, cost_a, cost_b, cost_c,
                       cost_d, cost_e))
        else:
            game.deleteUploadedSample(sample_id)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    if shouldJumpToNextTurn() == True:
        continue

    go_to_samples()
    get_rank()

    go_to_diagnosis()
    get_diagnose()
    upload_sample()

    go_to_molecules()
    get_molecules()

    go_to_laboratory()
    extract_medicine()

    cleanUp()

    game.turn = game.turn + 1
    print("DEBUG: turn =", game.turn, file=sys.stderr)
