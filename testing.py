import unittest
import extractexcel as excel
import patternchecker as ptchk
import csv



class Test(unittest.TestCase):

    def setUp(self):
        myfile = open(
            '/home/beliefs22/python/DeIdentification-Tool/csvs/test_csv_2.csv', 'r')
        excelreader = csv.reader(myfile)
        self.fixture = excel.Excel(excelreader)
        myfile.close()
        self.master_allowed, self.master_not_allowed, \
                             self.master_indeterminate = self.fixture.one_pass()
 
    def tearDown(self):
        del self.fixture

    def test_one_pass(self):
        #simulates what words should be categorized as after program runs
        allowed = ['12','315','333']
        not_allowed = ['Seth','Pitts','3/20/2015','4/1/2015',
                       'Matthews','4/15/2015']
        indeterminate = ['Sp1','Sp2','Bobby','Jones','Sp3','Beilin']        
        #True only if out put matches expected output
        one_pass_pass = self.master_allowed == allowed and \
                        self.master_not_allowed == not_allowed and \
                        self.master_indeterminate == indeterminate
      
        if not one_pass_pass:
            print "allowed is", allowed, self.master_allowed
            print
            print "not allowed is", not_allowed, self.master_not_allowed
            print
            print "indeterminate is", indeterminate, self.master_indeterminate  
        self.failUnless(one_pass_pass,"all list should be equal")

    def test_deidentify(self):
        #Simulate user input to create file specific dictionaries
        user_allowed = ['Sp1', 'Sp2', 'Sp3']
        user_not_allowed = ['Bobby','Jones']
        allowed_before = self.master_allowed[:]
        not_allowed_before = self.master_not_allowed[:]
        indeterminate_before = self.master_indeterminate[:]
        self.master_not_allowed += user_not_allowed

        for word in user_allowed:
            self.master_indeterminate.remove(word)# remove allowed words
            #run test with simulated input
        self.fixture.deidentify(self.master_not_allowed,
                                self.master_indeterminate)
        #what data should look like after it has been cleaned
        clean_data = ['Sp1,[REDACTED],[REDACTED],[REDACTED],12',
                      'Sp2,[REDACTED],[REDACTED],[REDACTED],315',
                      'Sp3,Beilin[INDETER],[REDACTED],[REDACTED],-333']
        
        deidentify_pass = True
        #True only if output matched expected output
        for index, subject in enumerate(self.fixture.get_subjects()):
            subject_pass = subject.get_clean_data() == clean_data[index]
            if not subject_pass:
                deidentify_pass = False
                print "expecting %s \n got %s " % (clean_data[index],
                                                subject.get_clean_data())
        if not deidentify_pass:
            print "Master allowed before simulated input\n %s\n after\n %s" \
                  % (allowed_before, self.master_allowed)
            print "Master not allowed before simulated input\n %s\n after\n %s" \
                  % (not_allowed_before, self.master_not_allowed)
            print "Master indeterminate before simulated input\n %s\n after\n %s" \
                  % (indeterminate_before, self.master_indeterminate)                

        self.failUnless(deidentify_pass, "Final Data not correct")

    def test_pattern(self):
        #test to see if pattern check finds obvious names
        dictionary = ptchk.Dictionary()
        allowed, not_allowed, indeterminate = \
                 ptchk.check_for_words("Aristotle Lewis Rajah Seth",
                                       dictionary.export_dicts())
        #apparently no one names their children aristole or rajah in america
        expected_allowed = ['Aristotle', 'Rajah']
        expected_not_allowed = ['Seth']
        expected_indeterminate = ['Lewis']
        #True only if output matches expected output
        pattern_pass = allowed == expected_allowed and \
                      not_allowed == expected_not_allowed and \
                      indeterminate == expected_indeterminate

        if not pattern_pass:
            print "expected allowed:\n %s\n got\n %s" \
                  % (expected_allowed, allowed)
            print "expected not allowed:\n %s\n got\n %s" \
                  % (expected_not_allowed, not_allowed)
            print "expeted indeterminate:\n %s\n got\n %s" \
                  % (expected_indeterminate, indeterminate)

        self.failUnless(pattern_pass, "Unexpected pattern match")       
        

if __name__ =='__main__':
    unittest.main()
