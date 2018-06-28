
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftIMPLIESIFFleftORANDrightNOTAND ASSIGN COMMA COMMENT CONTROL DCOL ENVIRONMENT EQUALS F FALSE G GOAL GUARD IFF IMPLIES INIT LB MODULE NAME NEXT NOT OR PROPF RB SEMICOLON TRUE U UPDATE X input : MODULE NAME CONTROL var_y INIT init_y UPDATE update_y GOAL goal_forminput : MODULE ENVIRONMENT CONTROL var_y INIT init_y UPDATE update_yinput : input input input : input PROPF prop_form var_y : NAMEvar_y : var_y COMMA var_yinit_y : DCOL init_command\n                | init_y DCOL init_commandinit_command : init_condition ASSIGN init_next_stateinit_condition : TRUEinit_next_state : NAME NEXT EQUALS TRUEinit_next_state : NAME NEXT EQUALS FALSEinit_next_state : init_next_state COMMA init_next_stateinit_next_state : init_next_state SEMICOLONupdate_command : update_condition ASSIGN update_next_stateupdate_y : DCOL update_command\n                | update_y DCOL update_commandupdate_condition : formula_guardupdate_condition : update_condition COMMA update_conditionformula_guard : NAMEformula_guard : TRUEformula_guard : FALSEformula_guard : formula_guard OR formula_guardformula_guard : formula_guard AND formula_guardformula_guard : formula_guard IMPLIES formula_guardformula_guard : formula_guard IFF formula_guardformula_guard : NOT formula_guardformula_guard : LB formula_guard RBupdate_next_state : NAME NEXT EQUALS formula_assignupdate_next_state : update_next_state COMMA update_next_stateupdate_next_state : update_next_state SEMICOLONformula_assign : NAMEformula_assign : TRUEformula_assign : FALSEformula_assign : formula_assign OR formula_assignformula_assign : formula_assign AND formula_assignformula_assign : formula_assign IMPLIES formula_assignformula_assign : formula_assign IFF formula_assignformula_assign : NOT formula_assignformula_assign : LB formula_assign RBgoal_form : DCOL gf SEMICOLONgf : NAMEgf : TRUEgf : FALSEgf : gf OR gfgf : gf AND gfgf : gf IMPLIES gfgf : gf IFF gfgf : G gfgf : F gfgf : X gfgf : gf U gfgf : NOT gfgf : LB gf RBprop_form : DCOL pf SEMICOLONpf : NAMEpf : TRUEpf : FALSEpf : pf OR pfpf : pf AND pfpf : pf IMPLIES pfpf : pf IFF pfpf : G pfpf : F pfpf : X pfpf : pf U pfpf : NOT pfpf : LB pf RB'
    
_lr_action_items = {'ENVIRONMENT':([1,],[4,]),'IFF':([14,15,19,22,26,27,28,35,36,41,42,43,44,45,46,60,63,66,67,79,80,84,85,89,92,96,97,98,99,100,103,104,105,112,113,119,120,121,122,123,124,127,128,130,132,133,138,139,140,141,142,143,],[-58,-56,32,-57,32,32,32,32,-67,-68,-60,-61,-62,32,-59,-22,76,-21,-20,76,-27,-44,-42,109,-43,-24,-26,-25,-23,-28,109,109,109,109,-53,-54,-46,-47,-48,109,-45,-34,-32,136,-33,136,-39,-40,-36,-37,-38,-35,]),'TRUE':([10,16,17,18,20,21,29,30,32,33,34,38,48,54,58,64,65,72,73,75,76,77,78,86,87,88,90,91,101,106,107,109,110,111,125,129,131,134,135,136,137,],[22,22,22,22,22,22,22,22,22,22,22,50,50,66,66,66,66,92,66,66,66,66,66,92,92,92,92,92,118,92,92,92,92,92,132,132,132,132,132,132,132,]),'CONTROL':([3,4,],[7,8,]),'LB':([10,16,17,18,20,21,29,30,32,33,34,54,58,64,65,72,73,75,76,77,78,86,87,88,90,91,106,107,109,110,111,125,129,131,134,135,136,137,],[17,17,17,17,17,17,17,17,17,17,17,64,64,64,64,87,64,64,64,64,64,87,87,87,87,87,87,87,87,87,87,129,129,129,129,129,129,129,]),'SEMICOLON':([14,15,19,22,26,28,35,36,41,42,43,44,45,46,69,82,84,85,89,92,95,102,103,105,112,113,115,117,118,119,120,121,122,123,124,126,127,128,130,132,138,139,140,141,142,143,],[-58,-56,31,-57,-64,-63,-65,-67,-68,-60,-61,-62,-66,-59,82,-14,-44,-42,108,-43,115,82,-50,-49,-51,-53,-31,-12,-11,-54,-46,-47,-48,-52,-45,115,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'DCOL':([5,23,25,37,40,47,49,52,53,55,57,59,62,69,70,82,95,102,115,117,118,126,127,128,130,132,138,139,140,141,142,143,],[10,38,38,48,48,54,-7,54,58,-8,58,72,-16,-9,-17,-14,-15,-13,-31,-12,-11,-30,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'NEXT':([68,94,],[81,114,]),'INIT':([11,12,13,39,],[-5,23,25,-6,]),'COMMA':([11,12,13,39,60,61,63,66,67,69,80,82,93,95,96,97,98,99,100,102,115,117,118,126,127,128,130,132,138,139,140,141,142,143,],[-5,24,24,24,-22,73,-18,-21,-20,83,-27,-14,73,116,-24,-26,-25,-23,-28,83,-31,-12,-11,116,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'RB':([14,15,22,26,27,28,35,36,41,42,43,44,45,46,60,66,67,79,80,84,85,92,96,97,98,99,100,103,104,105,112,113,119,120,121,122,123,124,127,128,132,133,138,139,140,141,142,143,],[-58,-56,-57,-64,41,-63,-65,-67,-68,-60,-61,-62,-66,-59,-22,-21,-20,100,-27,-44,-42,-43,-24,-26,-25,-23,-28,-50,119,-49,-51,-53,-54,-46,-47,-48,-52,-45,-34,-32,-33,139,-39,-40,-36,-37,-38,-35,]),'ASSIGN':([50,51,60,61,63,66,67,80,93,96,97,98,99,100,],[-10,56,-22,74,-18,-21,-20,-27,-19,-24,-26,-25,-23,-28,]),'$end':([2,6,9,31,57,62,70,71,95,108,115,126,127,128,130,132,138,139,140,141,142,143,],[0,-3,-4,-55,-2,-16,-17,-1,-15,-41,-31,-30,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'PROPF':([2,6,9,31,57,62,70,71,95,108,115,126,127,128,130,132,138,139,140,141,142,143,],[5,5,-4,-55,-2,-16,-17,-1,-15,-41,-31,-30,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'IMPLIES':([14,15,19,22,26,27,28,35,36,41,42,43,44,45,46,60,63,66,67,79,80,84,85,89,92,96,97,98,99,100,103,104,105,112,113,119,120,121,122,123,124,127,128,130,132,133,138,139,140,141,142,143,],[-58,-56,30,-57,30,30,30,30,-67,-68,-60,-61,-62,30,-59,-22,77,-21,-20,77,-27,-44,-42,107,-43,-24,-26,-25,-23,-28,107,107,107,107,-53,-54,-46,-47,-48,107,-45,-34,-32,135,-33,135,-39,-40,-36,-37,-38,-35,]),'G':([10,16,17,18,20,21,29,30,32,33,34,72,86,87,88,90,91,106,107,109,110,111,],[18,18,18,18,18,18,18,18,18,18,18,88,88,88,88,88,88,88,88,88,88,88,]),'F':([10,16,17,18,20,21,29,30,32,33,34,72,86,87,88,90,91,106,107,109,110,111,],[16,16,16,16,16,16,16,16,16,16,16,86,86,86,86,86,86,86,86,86,86,86,]),'UPDATE':([37,40,49,55,69,82,102,117,118,],[47,52,-7,-8,-9,-14,-13,-12,-11,]),'MODULE':([0,2,6,9,31,57,62,70,71,95,108,115,126,127,128,130,132,138,139,140,141,142,143,],[1,1,1,-4,-55,-2,-16,-17,-1,-15,-41,-31,-30,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'EQUALS':([81,114,],[101,125,]),'U':([14,15,19,22,26,27,28,35,36,41,42,43,44,45,46,84,85,89,92,103,104,105,112,113,119,120,121,122,123,124,],[-58,-56,33,-57,33,33,33,33,-67,-68,-60,-61,-62,33,-59,-44,-42,110,-43,110,110,110,110,-53,-54,-46,-47,-48,110,-45,]),'X':([10,16,17,18,20,21,29,30,32,33,34,72,86,87,88,90,91,106,107,109,110,111,],[20,20,20,20,20,20,20,20,20,20,20,90,90,90,90,90,90,90,90,90,90,90,]),'GOAL':([53,62,70,95,115,126,127,128,130,132,138,139,140,141,142,143,],[59,-16,-17,-15,-31,-30,-34,-32,-29,-33,-39,-40,-36,-37,-38,-35,]),'AND':([14,15,19,22,26,27,28,35,36,41,42,43,44,45,46,60,63,66,67,79,80,84,85,89,92,96,97,98,99,100,103,104,105,112,113,119,120,121,122,123,124,127,128,130,132,133,138,139,140,141,142,143,],[-58,-56,29,-57,29,29,29,29,-67,-68,-60,29,29,29,-59,-22,75,-21,-20,75,-27,-44,-42,106,-43,-24,75,75,-23,-28,106,106,106,106,-53,-54,-46,106,106,106,-45,-34,-32,134,-33,134,-39,-40,-36,134,134,-35,]),'FALSE':([10,16,17,18,20,21,29,30,32,33,34,54,58,64,65,72,73,75,76,77,78,86,87,88,90,91,101,106,107,109,110,111,125,129,131,134,135,136,137,],[14,14,14,14,14,14,14,14,14,14,14,60,60,60,60,84,60,60,60,60,60,84,84,84,84,84,117,84,84,84,84,84,127,127,127,127,127,127,127,]),'NAME':([1,7,8,10,16,17,18,20,21,24,29,30,32,33,34,54,56,58,64,65,72,73,74,75,76,77,78,83,86,87,88,90,91,106,107,109,110,111,116,125,129,131,134,135,136,137,],[3,11,11,15,15,15,15,15,15,11,15,15,15,15,15,67,68,67,67,67,85,67,94,67,67,67,67,68,85,85,85,85,85,85,85,85,85,85,94,128,128,128,128,128,128,128,]),'NOT':([10,16,17,18,20,21,29,30,32,33,34,54,58,64,65,72,73,75,76,77,78,86,87,88,90,91,106,107,109,110,111,125,129,131,134,135,136,137,],[21,21,21,21,21,21,21,21,21,21,21,65,65,65,65,91,65,65,65,65,65,91,91,91,91,91,91,91,91,91,91,131,131,131,131,131,131,131,]),'OR':([14,15,19,22,26,27,28,35,36,41,42,43,44,45,46,60,63,66,67,79,80,84,85,89,92,96,97,98,99,100,103,104,105,112,113,119,120,121,122,123,124,127,128,130,132,133,138,139,140,141,142,143,],[-58,-56,34,-57,34,34,34,34,-67,-68,-60,34,34,34,-59,-22,78,-21,-20,78,-27,-44,-42,111,-43,-24,78,78,-23,-28,111,111,111,111,-53,-54,-46,111,111,111,-45,-34,-32,137,-33,137,-39,-40,-36,137,137,-35,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'init_command':([38,48,],[49,55,]),'init_next_state':([56,83,],[69,102,]),'update_condition':([54,58,73,],[61,61,93,]),'update_command':([54,58,],[62,70,]),'init_y':([23,25,],[37,40,]),'formula_guard':([54,58,64,65,73,75,76,77,78,],[63,63,79,80,63,96,97,98,99,]),'update_y':([47,52,],[53,57,]),'formula_assign':([125,129,131,134,135,136,137,],[130,133,138,140,141,142,143,]),'prop_form':([5,],[9,]),'update_next_state':([74,116,],[95,126,]),'goal_form':([59,],[71,]),'gf':([72,86,87,88,90,91,106,107,109,110,111,],[89,103,104,105,112,113,120,121,122,123,124,]),'pf':([10,16,17,18,20,21,29,30,32,33,34,],[19,26,27,28,35,36,42,43,44,45,46,]),'var_y':([7,8,24,],[12,13,39,]),'input':([0,2,6,],[2,6,6,]),'init_condition':([38,48,],[51,51,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> input","S'",1,None,None,None),
  ('input -> MODULE NAME CONTROL var_y INIT init_y UPDATE update_y GOAL goal_form','input',10,'p_input_1','parsrml.py',145),
  ('input -> MODULE ENVIRONMENT CONTROL var_y INIT init_y UPDATE update_y','input',8,'p_input_2','parsrml.py',171),
  ('input -> input input','input',2,'p_input_3','parsrml.py',183),
  ('input -> input PROPF prop_form','input',3,'p_input_4','parsrml.py',186),
  ('var_y -> NAME','var_y',1,'p_var_y_1','parsrml.py',194),
  ('var_y -> var_y COMMA var_y','var_y',3,'p_var_y_2','parsrml.py',199),
  ('init_y -> DCOL init_command','init_y',2,'p_init_y_1','parsrml.py',205),
  ('init_y -> init_y DCOL init_command','init_y',3,'p_init_y_1','parsrml.py',206),
  ('init_command -> init_condition ASSIGN init_next_state','init_command',3,'p_init_command_1','parsrml.py',223),
  ('init_condition -> TRUE','init_condition',1,'p_init_condition_1','parsrml.py',226),
  ('init_next_state -> NAME NEXT EQUALS TRUE','init_next_state',4,'p_init_next_state_1','parsrml.py',232),
  ('init_next_state -> NAME NEXT EQUALS FALSE','init_next_state',4,'p_init_next_state_2','parsrml.py',237),
  ('init_next_state -> init_next_state COMMA init_next_state','init_next_state',3,'p_init_next_state_3','parsrml.py',243),
  ('init_next_state -> init_next_state SEMICOLON','init_next_state',2,'p_init_next_state_4','parsrml.py',246),
  ('update_command -> update_condition ASSIGN update_next_state','update_command',3,'p_update_command_1','parsrml.py',251),
  ('update_y -> DCOL update_command','update_y',2,'p_update_y_1','parsrml.py',258),
  ('update_y -> update_y DCOL update_command','update_y',3,'p_update_y_1','parsrml.py',259),
  ('update_condition -> formula_guard','update_condition',1,'p_update_condition_1','parsrml.py',277),
  ('update_condition -> update_condition COMMA update_condition','update_condition',3,'p_update_condition_2','parsrml.py',280),
  ('formula_guard -> NAME','formula_guard',1,'p_formula_guard_1','parsrml.py',285),
  ('formula_guard -> TRUE','formula_guard',1,'p_formula_guard_2','parsrml.py',290),
  ('formula_guard -> FALSE','formula_guard',1,'p_formula_guard_3','parsrml.py',296),
  ('formula_guard -> formula_guard OR formula_guard','formula_guard',3,'p_formula_guard_4','parsrml.py',302),
  ('formula_guard -> formula_guard AND formula_guard','formula_guard',3,'p_formula_guard_5','parsrml.py',307),
  ('formula_guard -> formula_guard IMPLIES formula_guard','formula_guard',3,'p_formula_guard_6','parsrml.py',312),
  ('formula_guard -> formula_guard IFF formula_guard','formula_guard',3,'p_formula_guard_7','parsrml.py',317),
  ('formula_guard -> NOT formula_guard','formula_guard',2,'p_formula_guard_8','parsrml.py',322),
  ('formula_guard -> LB formula_guard RB','formula_guard',3,'p_formula_guard_9','parsrml.py',327),
  ('update_next_state -> NAME NEXT EQUALS formula_assign','update_next_state',4,'p_update_next_state_1','parsrml.py',333),
  ('update_next_state -> update_next_state COMMA update_next_state','update_next_state',3,'p_update_next_state_2','parsrml.py',339),
  ('update_next_state -> update_next_state SEMICOLON','update_next_state',2,'p_update_next_state_3','parsrml.py',342),
  ('formula_assign -> NAME','formula_assign',1,'p_formula_assign_1','parsrml.py',347),
  ('formula_assign -> TRUE','formula_assign',1,'p_formula_assign_2','parsrml.py',352),
  ('formula_assign -> FALSE','formula_assign',1,'p_formula_assign_3','parsrml.py',358),
  ('formula_assign -> formula_assign OR formula_assign','formula_assign',3,'p_formula_assign_4','parsrml.py',364),
  ('formula_assign -> formula_assign AND formula_assign','formula_assign',3,'p_formula_assign_5','parsrml.py',369),
  ('formula_assign -> formula_assign IMPLIES formula_assign','formula_assign',3,'p_formula_assign_6','parsrml.py',374),
  ('formula_assign -> formula_assign IFF formula_assign','formula_assign',3,'p_formula_assign_7','parsrml.py',379),
  ('formula_assign -> NOT formula_assign','formula_assign',2,'p_formula_assign_8','parsrml.py',384),
  ('formula_assign -> LB formula_assign RB','formula_assign',3,'p_formula_assign_9','parsrml.py',389),
  ('goal_form -> DCOL gf SEMICOLON','goal_form',3,'p_goal_form_1','parsrml.py',394),
  ('gf -> NAME','gf',1,'p_gf_1','parsrml.py',401),
  ('gf -> TRUE','gf',1,'p_gf_2','parsrml.py',407),
  ('gf -> FALSE','gf',1,'p_gf_3','parsrml.py',411),
  ('gf -> gf OR gf','gf',3,'p_gf_4','parsrml.py',415),
  ('gf -> gf AND gf','gf',3,'p_gf_5','parsrml.py',419),
  ('gf -> gf IMPLIES gf','gf',3,'p_gf_6','parsrml.py',423),
  ('gf -> gf IFF gf','gf',3,'p_gf_7','parsrml.py',428),
  ('gf -> G gf','gf',2,'p_gf_8','parsrml.py',432),
  ('gf -> F gf','gf',2,'p_gf_9','parsrml.py',436),
  ('gf -> X gf','gf',2,'p_gf_10','parsrml.py',440),
  ('gf -> gf U gf','gf',3,'p_gf_11','parsrml.py',444),
  ('gf -> NOT gf','gf',2,'p_gf_12','parsrml.py',448),
  ('gf -> LB gf RB','gf',3,'p_gf_13','parsrml.py',452),
  ('prop_form -> DCOL pf SEMICOLON','prop_form',3,'p_prop_form_1','parsrml.py',460),
  ('pf -> NAME','pf',1,'p_pf_1','parsrml.py',465),
  ('pf -> TRUE','pf',1,'p_pf_2','parsrml.py',471),
  ('pf -> FALSE','pf',1,'p_pf_3','parsrml.py',475),
  ('pf -> pf OR pf','pf',3,'p_pf_4','parsrml.py',479),
  ('pf -> pf AND pf','pf',3,'p_pf_5','parsrml.py',483),
  ('pf -> pf IMPLIES pf','pf',3,'p_pf_6','parsrml.py',487),
  ('pf -> pf IFF pf','pf',3,'p_pf_7','parsrml.py',492),
  ('pf -> G pf','pf',2,'p_pf_8','parsrml.py',496),
  ('pf -> F pf','pf',2,'p_pf_9','parsrml.py',500),
  ('pf -> X pf','pf',2,'p_pf_10','parsrml.py',504),
  ('pf -> pf U pf','pf',3,'p_pf_11','parsrml.py',508),
  ('pf -> NOT pf','pf',2,'p_pf_12','parsrml.py',512),
  ('pf -> LB pf RB','pf',3,'p_pf_13','parsrml.py',516),
]