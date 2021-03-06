''' 
This is the base class for all indicators. 
To make a new Indicator, you need to make a class that inherit this class.
Example is given in simple_trend.py which makes a SimpleTrend class.
'''

from MarketAdapter.security_market_view import SecurityMarketViewChangeListener
from indicator_listener import IndicatorListenerPair
#from CommonTradeUtils.market_update_manager import MarketUpdateManager

class CommonIndicator(SecurityMarketViewChangeListener):
    concise_indicator_description_map_ = dict()
    def __init__(self, *args):
        self.concise_indicator_description_ = ""
        self.indicator_listener_pairs_ = []
        self.unweighted_indicator_listener_pairs_ = []
        self.indicator_value_ = 0.0
        self.is_ready_ = False
        self.data_interupted_ = False
        self.base_price_type_ = 'MidPrice'
        if len(args) == 3:
            self.watch_ = args[0]
            self.concise_indicator_description_ = args[1]
            self.price_type = args[2]
        if len(args) == 2:
            self.watch_ = args[0]
            self.concise_indicator_description_ = args[1]
             
    def SetBasepxPxtype (self, smv, base_px_type):
        self.base_price_type = base_px_type
 
    def OnGlobalPositionChange ( self, security_id, new_global_pos):
        return
    
    def ConciseIndicatorDescription (self ):
        return  self.concise_indicator_description_
    
    def IsIndicatorReady(self):
        return self.is_ready_
    
    def IsDataInterrupted(self):
        return self.data_interupted_
    
    def IndicatorValue(self, is_ready):
        if is_ready :
            return self.indicator_value_
        else :
            return 0.0
    
    def WhyNotReady(self):
        return
    
    def GetReadinessRequired(self, r_dep_shortcode_, tokens_):
        return True
#         core_shortcode_vec_= []
#         core_shortcodes.GetCoreShortcodes(r_dep_shortcode_, core_shortcode_vec_)
#         if tokens_[3] in core_shortcode_vec_:
#             return True
#         else:
#             return False
    
#     def SubscribeDataInterrupts(self, _market_update_manager_):
#         return
    
#     def OnIndicatorUpdate(self, _indicator_index_ , _new_value_):
#         return
 
    def AddIndicatorListener(self, _indicator_index_, _indicator_listener_,  _node_value_):   
        if _indicator_listener_ is not None and not self.IsWeightedListenerPresent(_indicator_listener_):
            _new_indicator_listener_pair_ = IndicatorListenerPair(_indicator_index_, _indicator_listener_, _node_value_)
            self.indicator_listener_pairs_.append(_new_indicator_listener_pair_)
    
#     def UpdateIndicatorListenerWeight(self, _indicator_listener_, _node_value_):
#         for x in range(len(self.indicator_listener_pairs_)):
#             if self.indicator_listener_pairs_[x].indicator_listener_ == _indicator_listener_:
#                 self.indicator_listener_pairs_[x].node_value_ = _node_value_
    
#     def MultiplyIndicatorListenerWeight (self, _indicator_listener_, _node_value_mult_factor_ ):
#         for x in range(len(self.indicator_listener_pairs_)):
#             if self.indicator_listener_pairs_[x].indicator_listener_ == _indicator_listener_:
#                 self.indicator_listener_pairs_[x].node_value_ *= _node_value_mult_factor_
  
#     def GetIndicatorListenerWeight (self, _indicator_listener_):
#         for x in range(len(self.indicator_listener_pairs_)):
#             if self.indicator_listener_pairs_[x].indicator_listener_ == _indicator_listener_:
#                 return self.indicator_listener_pairs_[x].node_value_
#         return -100000000
    
    def IsWeightedListenerPresent(self, _indicator_listener_):
        for x in range(len(self.indicator_listener_pairs_)):
            if self.indicator_listener_pairs_[x].indicator_listener_ == _indicator_listener_:
                return True
        return False
    
#     def AddUnweightedIndicatorListener(self,_indicator_index_, _indicator_listener__ ):
#         if _indicator_listener__ is not None and self.IsUnweightedListenerPresent ( _indicator_listener__ ) == False :
#             _new_unweighted_indicator_listener_pair_ = UnweightedIndicatorListenerPair( _indicator_index_, _indicator_listener__ )
#             self.unweighted_indicator_listener_pairs_.append(_new_unweighted_indicator_listener_pair_) 
          
#     def IsUnweightedListenerPresent(self, _indicator_listener_):
#         for x in range(len(self.unweighted_indicator_listener_pairs_)):
#             if self.unweighted_indicator_listener_pairs_[x].indicator_listener_ == _indicator_listener_:
#                 return True
#         return False
    
    def NotifyIndicatorListeners(self, _indicator_value_):
        for x in range(len(self.indicator_listener_pairs_)):
            self.indicator_listener_pairs_[x].OnIndicatorUpdate(_indicator_value_) 
#         for x in range(len(self.unweighted_indicator_listener_pairs_)):
#             self.unweighted_indicator_listener_pairs_[x].OnIndicatorUpdate(_indicator_value_)
