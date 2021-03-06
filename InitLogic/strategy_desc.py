from CommonTradeUtils.watch import Watch

class StrategyLine():

    def __init__(self):
        self.dep_shortcode_ = "invalid"
        self.strategy_name_ = "invalid"
        self.model_filename_ = "invalid"
        self.param_filename_ = "invalid"
        self.trading_start_time_ = 0
        self.trading_start_time_mfm_ = 8*60*60*1000
        self.trading_end_time_ = 0
        self.trading_end_time_mfm_ = 8*60*60*1000
        self.exec_ = None
        self.runtime_id_ = 0
        self.dep_market_view_ = None
        self.base_trader_ = None
        self.strategy_full_line_ = ""

'''TODO: Remove strategy_vec_[]'''
class StrategyDesc():
    
    def __init__(self, _strategy_desc_filename_, _tradingdate_):
        self.strategy_desc_filename_ = _strategy_desc_filename_
        self.strategy_vec_ = []
        strategy_desc_file_ = open(self.strategy_desc_filename_)
        for line_ in strategy_desc_file_:
            tokens_ = line_.split()
            if len(tokens_) >= 7 and tokens_[0] == "STRATEGYLINE":
                strategy_line_ = StrategyLine()
                strategy_line_.dep_shortcode_ = tokens_[1]
                strategy_line_.strategy_name_ = tokens_[2]
                strategy_line_.model_filename_ = tokens_[3]
                strategy_line_.param_filename_ = tokens_[4]
                strategy_line_.trading_start_time_ = tokens_[5]
                strategy_line_.trading_start_time_mfm_ = Watch.GetMSecsFromUTC(int(tokens_[5]))
                strategy_line_.trading_end_time_ = tokens_[6]
                strategy_line_.trading_end_time_mfm_= Watch.GetMSecsFromUTC(int(tokens_[6]))
                strategy_line_.runtime_id_ = int(tokens_[7])
                strategy_line_.strategy_full_line_ = line_
                for i in range(len(self.strategy_vec_)):
                    if self.strategy_vec_[i].runtime_id_ == strategy_line_.runtime_id_:
                        exit()
                self.strategy_vec_.append(strategy_line_)
                
    def Dump(self):
        print('----------------------------------')
        print('Dumping StrategyDesc:')
        print(self.strategy_vec_[0].dep_shortcode_)
        print(self.strategy_vec_[0].strategy_name_)
        print(self.strategy_vec_[0].model_filename_)
        print(self.strategy_vec_[0].param_filename_)
        print(self.strategy_vec_[0].trading_start_time_)
        print(self.strategy_vec_[0].trading_start_time_mfm_)
        print(self.strategy_vec_[0].trading_end_time_)
        print(self.strategy_vec_[0].trading_end_time_mfm_)
        print(self.strategy_vec_[0].runtime_id_)
        print(self.strategy_vec_[0].strategy_full_line_)
        print('----------------------------------')
        
    def GetMinStartTime(self):
        return self.strategy_vec_[0].trading_start_time_mfm_
    
    def GetMaxEndTime(self):
        return self.strategy_vec_[0].trading_end_time_mfm_