"""
Provides function that can be called after an adjustment to elo.py
to update last season's results and thus be used to start starting
team ELOs for current season

Notes:
- ideally we have a script here that can be called after changing
elo.py and not have to worry about anything else

MANUAL STEPS:
- run prev_season.py -> creates:
    - backend/old_data/20202021seasonPROCESSED.csv
    - backend/old_data/20202021seasonELORESULTS.csv
- elo_adj in eda.py uses get_elo_df in prev_season.py
    - creates backend/old_data/20202021seasonELOWITHADJ.csv
- elo_system calls get_starting_elo_dict in elo_primer.py
    - get_starting_elo_dict reads 20202021seasonELOWITHADJ.csv
    - returns starting_team_elo_dict
"""
