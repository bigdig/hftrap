'''Common Class for OrderManager and SimMarketMaker'''
class BaseOrder:
    
    def __init__(self):
        self.security_name_ = ''
        self.buysell_ = 0
        self.price_ = 0
        self.size_remaining_ = 0
        self.size_executed_ = 0
        self.size_requested_ = 0
        self.int_price_ = 0
        self.order_status_ = 'None'
        
        self.queue_size_ahead_ = 0
        self.queue_size_behind_ = 0
        #self.queue_orders_ahead_ = 0
        #self.queue_orders_behind_ = 0
        self.num_events_seen_ = 0
        #self.order_id_ = 0
        self.client_assigned_order_sequence_ = 0
        self.server_assigned_order_sequence_ = 0
        self.server_assigned_client_id_ = 0
        
        #self.min_order_size_ = 1

        #self.order_sequenced_time_ = 0
        #self.order_confirmation_time_ = 0
        #self.order_entry_time_ = 0
        #self.correct_update_time_ = False
        #self.priority_order_ = False
        
        self.canceled_ = False
        #self.replayed_ = False
        
    def dump(self):
        #print '------------------------------------'
        #print 'Dumping Order:'
        #print 'security_name_:\t\t'+self.security_name_
        print '(',
        print self.buysell_,
        #print 'price_:\t\t\t'+str(self.price_)
        print str(self.int_price_),
        print str(self.size_requested_),
        print str(self.size_remaining_),
        print str(self.size_executed_),
        #print 'order_status_:\t\t'+str(self.order_status_)
        
        print str(self.queue_size_ahead_),
        print str(self.queue_size_behind_),
        #self.queue_orders_ahead_ = 0
        #self.queue_orders_behind_ = 0
        print str(self.num_events_seen_),
        #self.order_id_ = 0
        #print 'caos_:\t\t\t'+str(self.client_assigned_order_sequence_)
        
        #print 'saoa_:\t\t\t'+str(self.server_assigned_order_sequence_)
        #print 'saci_:\t\t\t'+str(self.server_assigned_client_id_)
        
        #print '------------------------------------'
        print ')',
        #self.min_order_size_ = 1

        #self.order_sequenced_time_ = 0
        #self.order_confirmation_time_ = 0
        #self.order_entry_time_ = 0
        #self.correct_update_time_ = False
        #self.priority_order_ = False
        
        #self.canceled_ = False
        #self.replayed_ = False
        
    def security_name(self):
        return self.security_name_
    
    def buysell(self):
        return self.buysell_
    
    def price(self):
        return self.price_
    
    def size_remaining(self):
        return self.size_remaining_
    
    def size_executed(self):
        return self.size_executed_
    
    def size_requested(self):
        return self.size_requested_
    
    def int_price(self):
        return self.int_price_
    
    def order_status(self):
        return self.order_status_
    
    def canceled(self):
        return self.canceled_
    
    def replayed(self):
        return self.replayed_
    
    def client_assigned_order_sequence(self):
        return self.client_assigned_order_sequence_
    
    def server_assigned_order_sequence(self):
        return self.server_assigned_order_sequence_
        
    def server_assigned_client_id(self):
        return self.server_assigned_client_id_
    
    def ExecuteRemaining(self):
        t_size_remaining_ = self.size_remaining_
        self.size_remaining_ = 0
        self.size_executed_ += t_size_remaining_
        return t_size_remaining_
    
    def MatchPartial(self, _further_match_):
        t_size_possible_ = min(_further_match_, self.size_remaining_)
        self.size_executed_ += t_size_possible_
        self.size_remaining_ -= t_size_possible_
        return t_size_possible_
    
    def HandleCrossingTrade(self, _trade_size_, _posttrade_size_at_price_):
        if (self.num_events_seen_ < 1):
            return 0
        if (_trade_size_ > self.queue_size_ahead_): 
            _further_match_ = _trade_size_ - self.queue_size_ahead_
            t_size_executed_ = self.MatchPartial(_further_match_)
            return t_size_executed_
        else:
            self.queue_size_ahead_ -= _trade_size_
            self.Enqueue(_posttrade_size_at_price_) # since we have an estimate of the total_market_non_self_size at this level after this trade, we use it to adjust queue_size_ahead_ and queue_size_behind_
            return 0
    
    def Confirm(self):
        self.order_status_ = 'Conf'
        self.num_events_seen_ = 0
        
    def ConfirmNewSize(self, _new_size_):
        self.size_executed_ = self.size_requested_ - _new_size_
        self.size_remaining_ = _new_size_
        
    def CanBeCanceled(self):
        return not self.canceled_ and self.size_remaining_ > 0
        
    def IsConfirm(self):
        return self.order_status_ == 'Conf'
    
    def Enqueue(self, _queue_size_):
        if (self.num_events_seen_ == 0):
            self.queue_size_behind_ = 0
            self.queue_size_ahead_ = _queue_size_
            self.num_events_seen_ += 1
        else:
            '''Implement this'''
'''       
    def ResetQueue(self):
        
        
    def SendToTop(self): 
'''