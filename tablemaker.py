
import numpy as np

class Labs:
    
    
    def __init__(self, quantities, data, rounding_digits=None):
        """
        Physical quantities and corresponding units are given as a dictionary
        of quantity: unit pairs, while data is given as a 2D list (list of lists)
        -------------------------------------------------------------------------
        Parameters:
        
        quantities - dict
        data - 2D list of floats, ints or None types
        rounding_digits - None (default) or list of ints or None types
        -------------------------------------------------------------------------
        """
        
        # Handling input exceptions
        if not quantities or not data:
            raise ValueError("Empty input given!")
            
        elif not isinstance(quantities, dict):
            raise ValueError("Given quantities parameter is not a dict datatype!")
        
        for pair in quantities.items():
            if not isinstance(pair[0], str) or not isinstance(pair[1], str):
                raise ValueError("Given quantity: unit pairs are not strings!")
            
        if not isinstance(data, list):
            raise ValueError("Given data parameter is not a list datatype!")
        
        for lst in data:
            if not isinstance(lst, list):
                raise ValueError("Data does not contain list datatypes!")
            for val in lst:
                if not isinstance(val, (float, int)) and val:
                    raise ValueError("A list in data does not contain a number!")
                    
        if len(quantities) != len(data):
            raise ValueError("Length of quantities does not match the number of columns in data!")
        
        if rounding_digits:
            if not isinstance(rounding_digits, list):
                raise ValueError("Given rounding_digits parameter is not a list datatype!")
            
            if len(rounding_digits) != len(data):
                raise ValueError("Length of of rounding_digits is not the same as length of data")

            for val in rounding_digits:
                if not isinstance(val, int) and val:
                    raise ValueError("One of the digits in rounding_digits is not an int datatype!")
                    
        
        # Set class attributes
        self.quantities = quantities
        self.data = data
        self.m = len(max(data, key=len))
        self.n = len(data)
        
        if rounding_digits:
            self.rounding_digits = rounding_digits
        else:
            self.rounding_digits = [None]*self.n
            
        for i, lst in enumerate(data):
            self.data[i] += [None]*(self.m - len(lst))
        
        
    def first_nonzero(self, x):
        """
        Find postiion of the first nonzero digit in a number
        -------------------------------------------------------------------------
        Parameters:
        
        x - float, int or None
        -------------------------------------------------------------------------
        Returns:

        position - int
        ------------------------------------------------------------
        """
        
        # Handling input exceptions
        if x == None:
            return x
        
        if not x:
            return 0
        
        if not isinstance(x, (float, int)):
            raise ValueError("Given x parameter is not a float datatype!")
        
        # Calculation
        x = str(float(abs(x)))
        digits = [int(d) for d in x if d != "."]
        point_pos = x.find(".")
        position = next((i for i, d in enumerate(digits) if d), None)
        return position - point_pos + 1
        
        
    def prettify(self, x, digit):
        """
        Number x is rounded and formatter to given digit and returned 
        as a string with "," as a decimal point instead of "."
        -------------------------------------------------------------------------
        Parameters:
        
        x - float, int or None
        digit - int
        -------------------------------------------------------------------------
        Returns:
        
        num - str
        -------------------------------------------------------------------------
        """

        # Handling input exceptions
        if x == None:
            return x
        
        if not isinstance(x, (float, int)):
            raise ValueError("Given x parameter is not a float datatype!")

        if not isinstance(digit, int):
            raise ValueError("Given digit parameter is not an int datatype!")
            
        # Process
        formatter = "{:." + "{}".format(max(digit, 0)) + "f}"
        x = np.around(x, digit)
        return (formatter.format(x)).replace(".", ",")
    
    
    def stat_values(self, data):
        """
        Mean and standard error of each column is calculated and rounded appropriately
        -------------------------------------------------------------------------
        Parameters:
        
        data - 2D np.ndarray of floats, ints or Nones
        -------------------------------------------------------------------------
        """
        
        # Handling input exceptions
        if not isinstance(data, list):
            raise ValueError("Given data parameter is not a list datatype!")
            
        data = data.copy()
        for i, lst in enumerate(data):
            if not isinstance(lst, list):
                raise ValueError("Data array does not contain list datatypes!")
            
            data[i] = list(filter(None, data[i]))  # None datatypes prevent calculations
            for val in data[i]:
                if not isinstance(val, (float, int)):
                    raise ValueError("There is a non-number entry in data!")
                
        # Calculation
        self.means = [np.mean(col) for col in data]
        self.SEs = [np.std(col)/(len(col)**(1/2)) for col in data]
        
        # Calculate rounding digits + Rounding
        for i, x in enumerate(self.SEs):
            if not self.rounding_digits[i]:
                self.rounding_digits[i] = self.first_nonzero(x)
                
        for i in range(self.n):
            self.SEs[i] = self.prettify(self.SEs[i], self.rounding_digits[i])
            self.means[i] = self.prettify(self.means[i], self.rounding_digits[i])
    
    
    # Multiple functions designed for convenience purposes
    def hline(self):
        print("\\hline")
        
    def beginning(self, n):
        print("\\begin{table}[!ht]")
        print("\\centering")
        print("\\begin{tabular}" + "{|", end="")
        for i in range(n):
            print("r|", end="")
        print("}")
    
    def ending(self):
        print("\\end{tabular}")
        print("\\caption{}")
        print("\\label{tab:}")
        print("\\end{table}")
    
    
    # Core tablemaking function
    def make_table(self, count=True, stats=True):
        """
        Produces a simple table with columns, units, data points, optional order 
        count and optional statistical values (mean & standard error)
        -------------------------------------------------------------------------
        Parameters:
        
        count - Bool
        stats - Bool
        -------------------------------------------------------------------------
        """
        
        # Handling input exceptions
        if not isinstance(count, bool):
            raise ValueError("Given count parameter is not a boolean datatype!")
        
        if not isinstance(stats, bool):
            raise ValueError("Given stats parameter is not a boolean datatype!")
        
        self.stat_values(self.data)
        
        # Create basic LaTeX table layout
        if count:
            self.beginning(self.n + 1)
        else:
            self.beginning()
        self.hline()
        
        # Insert column headers (i.e. physical quantities & units)
        # Using specific LaTeX macros!! see: "sablona"
        if count:
            print("\\#", end=" & ")
        for i, var in enumerate(self.quantities):
            if i < self.n-1:
                print(f"\\tabh\u007b{var}\u007d\u007b{self.quantities[var]}\u007d", end=" & ")
            else:
                print(f"\\tabh\u007b{var}\u007d\u007b{self.quantities[var]}\u007d", end=" \\\\ \n")
        self.hline()
        self.hline()

        # Insert all values row by row
        for i in range(self.m):
            if count:
                print(i+1, end=" & ")
            for j, lst in enumerate(self.data[:-1]):
                if lst[i] == None:
                    print(" - ", end=" & ")
                else:
                    print(self.prettify(lst[i], self.rounding_digits[j]), end=" & ")
            if self.data[-1][i] == None:
                print(" - ", end=" \\\\ \n")
            else:
                print(self.prettify(self.data[-1][i], self.rounding_digits[-1]), end=" \\\\ \n")
            self.hline()

        # Print mean and standard error of each column if expected
        if stats:
            
            self.hline()
            print("$\\bar{x}$ & ", end="")
            for i in range(self.n - 1):
                print(self.means[i], end=" & ")
            print(self.means[-1], end=" \\\\ \n")
            
            self.hline()
            print("$\\sigma_0$ & ", end="")
            for i in range(self.n - 1):
                print(self.SEs[i], end=" & ")
            print(self.SEs[-1], end=" \\\\ \n")
            self.hline()
            
        self.ending()
