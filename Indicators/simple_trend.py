
from common_indicator import CommonIndicator
import math
from CDef import MathUtils
from MarketAdapter.security_market_view import SecurityMarketView
from MarketAdapter.shortcode_security_market_view_map import ShortcodeSecurityMarketViewMap

class SimpleTrend(CommonIndicator):
    
    def __init(self, watch,concise_indicator_description_,  _indep_market_view_, _fractional_seconds_, _price_type_):
        super(self, watch,concise_indicator_description_)
        self.trend_histroy_msecs = _fractional_seconds_ * 1000.0
        self.price_type = _price_type_
        self.indep_market_view = _indep_market_view_
        self.moving_avg_price = 0.0
        self.last_new_page_msecs_ = 0
        self.page_width_msecs_ = 500
        self.decay_page_factor_ = 0.95
        self.decay_vector_ = []
        self.inv_decay_sum_ = 0.05        
        self.decay_vector_sums_ = []        
        self.last_price_recorded_ = 0.0
        self.current_indep_price_ = 0.0
        self.SetTimeDecayWeights()


    def  CollectShortCodes(self, _shortcodes_affecting_this_indicator_,_ors_source_needed_vec_ , r_tokens_):
        if r_tokens_[3] not in _shortcodes_affecting_this_indicator_:
            _shortcodes_affecting_this_indicator_.append(r_tokens_[3])
    
    def GetUniqueInstance(self, r_watch_, r_tokens_, _basepx_pxtype_):
        #INDICATOR _this_weight_ _indicator_string_ _indep_market_view_ _fractional_seconds_ _price_type_
        return self.GetUniqueInstance2(self, r_watch_, ShortcodeSecurityMarketViewMap.StaticGetSecurityMarketView ( r_tokens_[3] ), (float)(r_tokens_[4]) ,r_tokens_[5] )
    
    def GetUniqueInstance2(self, r_watch_, _indep_market_view_,_fractional_seconds_, _price_type_ ):
        t_temp_oss_ = self.VarName() + " " + self._indep_market_view_.secname ( ) +  " " + _fractional_seconds_ + " " + _price_type_
        concise_indicator_description_ = t_temp_oss_
        if concise_indicator_description_ not in self.concise_indicator_description_map_.keys() : 
            self.concise_indicator_description_map_[concise_indicator_description_] = SimpleTrend ( r_watch_, concise_indicator_description_, _indep_market_view_, _fractional_seconds_, _price_type_ ) ;
        return self.concise_indicator_description_map_ [ concise_indicator_description_ ] ;

    def OnMarketUpdate(self,_security_id_, _market_update_info_ ):   
        self.current_indep_price_ = SecurityMarketView.GetPriceFromType ( self.price_type_, _market_update_info_ );
        if not self.is_ready and self.indep_market_view_.is_ready_complex(2):
            self.is_ready_ = True 
            self.InitializeValues ( )
        elif not self.data_interupted :
            if self.watch.msecs_from_midnight - self.last_new_page_msecs_ < self.page_width_msecs_ :
                self.moving_avg_price_ += self.inv_decay_sum_ * (self.current_indep_price_ - self.last_price_recorded_)
            else :
                num_pages_to_add_ = (int) (math.floor ( ( self.watch_.msecs_from_midnight - self.last_new_page_msecs_ ) / self.page_width_msecs_ ))
                if num_pages_to_add_ >= len(self.decay_vector_) :
                    self.InitializeValues()
                else :
                    if num_pages_to_add_ ==1 :
                        self.moving_avg_price_ = self.current_indep_price_ * self.inv_decay_sum_ + self.moving_avg_price_ * self.decay_vector_ [ 1 ]
                    else:
                        self.moving_avg_price_ = self.current_indep_price_ * self.inv_decay_sum_ + self.last_price_recorded_ * self.inv_decay_sum_ * self.decay_vector_sums_[ ( num_pages_to_add_ - 1 ) ] + self.moving_avg_price_*self.  decay_vector_ [ num_pages_to_add_ ]         
                    
                    self.last_new_page_msecs_ += ( num_pages_to_add_ * self.page_width_msecs_ ) ;
     
            self.last_price_recorded_ = self.current_indep_price_;    
            self.indicator_value_ = ( self.current_indep_price_ - self.moving_avg_price_ ) ;
            self.NotifyIndicatorListeners ( self.indicator_value_ )
    
    def SetTimeDecayWeights(self):
        kDecayLength = 20
        kMinPageWidth = 10
        kMaxPageWidth = 200
        self.page_width_msecs_ = min ( kMaxPageWidth, max( kMinPageWidth, ( self.trend_history_msecs_ / kDecayLength ) ) )
        number_fadeoffs_ = max ( 1, ( int ) (math.ceil( self.trend_history_msecs_ / self.page_width_msecs_) ) )
        self.decay_page_factor_ = MathUtils.CalcDecayFactor ( number_fadeoffs_ )
        self.decay_vector_ = []
        self.decay_vector_sums_ = []
        for i in range(2*(int)(number_fadeoffs_)):
            self.decay_vector_.append(pow ( self.decay_page_factor_, i ) )
        self.decay_vector_sums_.append(0)
        for i in range(2*(int)(number_fadeoffs_) - 1):
            self.decay_vector_sums_.append(self.decay_vector_sums_ [ i ] + self.decay_vector_ [ i + 1 ])
        self.inv_decay_sum_ = ( 1 - self.decay_page_factor_ )
     
    
    def InitializeValues(self):
        self.moving_avg_price_ = self.current_indep_price_ ;
        self.last_price_recorded_ = self.current_indep_price_ ;
        self.last_new_page_msecs_ = self.watch_.msecs_from_midnight - (self.watch_.msecs_from_midnight % self.page_width_msecs_)
        self.indicator_value_ = 0;

    
    def VarName(self):
        return "SimpleTrend"
    
    def OnMarketDataInterrupted(self,_security_id_, msecs_since_last_receive_ ):
        if self.indep_market_view_.security_id()==_security_id_ : 
            self.data_interrupted_ = True
            self.indicator_value_ = 0.0
            self.NotifyIndicatorListeners(self.indicator_value_)

    def OnMarketDataResumed(self, _security_id_):
        if self.indep_market_view_.security_id()==_security_id_ :
            self.InitializeValues()
            self.data_interrupted_ = False

    def OnTradePrint(self,_security_id_, _trade_print_info_, _market_update_info_ ):
        self.OnMarketUpdate(self,_security_id_, _market_update_info_ )
    
    