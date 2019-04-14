# written by Kazutoshi KAN, 2018
# -*- coding: utf-8 -*-
import re
from algorithm.graph import adj_matrix
from modelStructure.eviews_clean import clean

# filter non-variables in eviews model text 
# e.g. @movav, c_x(1), -2, dlog
def is_variable(s):
  return not re.match(r'@'  , s, re.I) and \
         not re.match(r'c_' , s, re.I) and \
         not re.match(r'\d' , s, re.I) and \
         not str.lower(s) in ['d', 'log', 'dlog', 'abs', 'exp']

def extract_variables(eq):
  eq = re.sub(r'\s', '', eq)
  terms = re.findall(r'@?\w+', eq)
  return set(filter(is_variable, terms))

def extract_structure(lines):
  # allvss = list of vars in each equation (including endo and exog)
  # vall   = endo and exog vars list
  # vendo  = endo vars list
  allvss = [extract_variables(eq) for eq in lines]
  vall   = set([v for vs in allvss for v in vs])
  vendo  = set([line.split(':')[0] for line in lines])
  return [allvss, vall, vendo, lines]

def load_modeltext(modelFilePath):
  # load eviews model text = list of 'id:equation'
  with open(modelFilePath, 'r') as fin:
    lines = fin.readlines()
    lines = clean(lines)
  return extract_structure(lines)

if __name__ == '__main__':

  modeltext = '''x  :log(x/y) = c_x(1)*y(-1)+c_x(2)*z(-1)+e_x
                 e_x:e_x = c_e_x(1)*e_x(-1)+v_x              
                 y  :log(y)   = c_y(1)*y+c_y(2)*z+w+e_y+a    
                 e_y:e_y = c_e_y(1)*e_y(-1)+v_y+z            
                 z  :log(z/y) = c_z(1)*y+c_z(2)*z+e_z        
                 e_z:e_z = c_e_z(1)*e_z(-1)+v_z              
                 w  :w        = 12*w(-1)+a+e_w                  
                 e_w:e_w      = @movav(e_w(-1),4)+v_w                  
                 a  :a        = a(-1) + w(1) + e_a           
                 e_a:e_a      = e_a(-1) + v_a                '''

  lines = clean(modeltext.split('\n'))

  [allvss, vall, vendo, lines] = extract_structure(lines)

  allvss = [sorted(vs) for vs in allvss]
  vall   = sorted(vall)
  vendo  = sorted(vendo)
  print('allvss = '+str(allvss))
  print('vall   = '+str(vall)  )
  print('vendo  = '+str(vendo) )

  #-> allvss = [['E_X', 'X', 'Y', 'Z'],
  #             ['E_X', 'V_X'], 
  #             ['A'  , 'E_Y', 'W', 'Y', 'Z'],
  #             ['E_Y', 'V_Y', 'Z'], 
  #             ['E_Z', 'Y', 'Z'], 
  #             ['E_Z', 'V_Z'],
  #             ['A'  , 'E_W', 'W'], 
  #             ['E_W', 'V_W'], 
  #             ['A'  , 'E_A', 'W'],
  #             ['E_A', 'V_A']]
  #-> vall   = ['A', 'E_A', 'E_W', 'E_X', 'E_Y', 'E_Z', 'V_A', 'V_W', 'V_X', 'V_Y', 'V_Z', 'W', 'X', 'Y', 'Z']
  #-> vendo  = ['A', 'E_A', 'E_W', 'E_X', 'E_Y', 'E_Z', 'W', 'X', 'Y', 'Z']

