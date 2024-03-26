class Manager():
    # precomputed heuristic maps for every possible cell
    hmaps: dict
    # precomputed seeker's pov maps for every possible cell
    seeker_povs: dict
    # precomputed hiders' pov maps for every possible cell
    hider_pov: dict
    def __init__(self, seeker, hiders, map_data):
        self.seeker = seeker
        self.hiders = hiders
        self.pings = []
        self.precompute_hmaps(map_data)
        self.precompute_hiders_povs
        
    def precompute_hmaps(self, map_data):
        pass
    
    def precompute_seeker_povs(self, map_data):
        pass
    
    def precompute_hiders_povs(self, map_data):
        pass