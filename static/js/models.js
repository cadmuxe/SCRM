

/**************************
     * Models
     **************************/
Customer = Ember.Object.extend({


        customer_url:function(){
            return "/customer/"+this.get('_id');
        }.property('_id'),
        save: function() {
            console.log(JSON.stringify(this));
            var request = $.ajax({
                type: "POST",
                url: "/api/customer/save",
                contentType:"application/json",
                data: JSON.stringify(this),
                success: function(data) {
                    return true;
                }
            });
            return 'ok';
        },
        get_content:function(){
            var rtn = ['type','manager','name','gender','birthday','memorial_days',
                'tags','sector','vocation','phone','email','company','home_addr',
            'contracts','likes','wishlist','remark','welfare','activities',
                'relevance_people','social','channel'];
            if (this.get('_id') != undefined){rtn.push('_id');}
            return this.getProperties(rtn);
        },
        view_how_long:function(){
            if (this.how_long != 10000){
                return this.how_long;
            }
            else{
                return "无联络信息";
            }
        }.property('how_long')

    });

Cal = Ember.Object.extend({
        start_date: function(key, value) {
            // getter
            if (arguments.length === 1) {
                var dt = this.get('start').split(' ');
                return dt[0];
            } else {
                var dt = this.get('start').split(' ');
                this.set('start', value+ " " + dt[1]);
                return value;
            }
        }.property('start'),
        start_time: function(key, value) {
            // getter
            if (arguments.length === 1) {
                var dt = this.get('start').split(' ');
                return dt[1];
            } else {
                var dt = this.get('start').split(' ');
                this.set('start', dt[0]+' ' + value);
                return value;
            }
        }.property('start'),
        end_date: function(key, value) {
            // getter
            if (arguments.length === 1) {
                var dt = this.get('end').split(' ');
                return dt[0];
            } else {
                var dt = this.get('end').split(' ');
                this.set('end', value+ " " + dt[1]);
                return value;
            }
        }.property('end'),
        end_time: function(key, value) {
            // getter
            if (arguments.length === 1) {
                var dt = this.get('end').split(' ');
                return dt[1];
            } else {
                var dt = this.get('end').split(' ');
                this.set('end', dt[0]+' ' + value);
                return value;
            }
        }.property('end'),

        save: function() {
            var request = $.ajax({
                type: "POST",
                url: "/api/cal/save",
                contentType:"application/json",
                data: JSON.stringify(this),
                success: function(data) {
                    return true;
                }
            });
            return 'ok';
        },
        done: function(){
            var request = $.ajax({
                type: "GET",
                url: "/api/cal/"+self._id+"/done",
                success: function(data) {
                    return true;
                }
            });
            return true;
        },
        not_done: function(){
            var request = $.ajax({
                type: "GET",
                url: "/api/cal/"+self._id+"/not_done",
                success: function(data) {
                    return true;
                }
            });
            return true;
        },
        get_content:function(){
            var rtn = ['type','manager','attend','title','start','end',
                'allDay','location','contact_type','spending','remark','finished'];
            if (this.get('_id') != undefined){rtn.push('_id');}
            return this.getProperties(rtn);
        }

    });

Memorial = Ember.Object.extend({

        save: function() {
            console.log(JSON.stringify(this));
            var request = $.ajax({
                type: "POST",
                url: "/api/memorial/save",
                contentType:"application/json",
                data: JSON.stringify(this),
                success: function(data) {
                    return true;
                }
            });
            return 'ok';
        }

    });

Contract = Ember.Object.extend({

        save: function() {
            console.log(JSON.stringify(this));
            var request = $.ajax({
                type: "POST",
                url: "/api/contract/save",
                contentType:"application/json",
                data: JSON.stringify(this),
                success: function(data) {
                    return true;
                }
            });
            return 'ok';
        }

    });

Project = Ember.Object.extend({

        save: function() {
            console.log(JSON.stringify(this));
            var request = $.ajax({
                type: "POST",
                url: "/api/project/save",
                contentType:"application/json",
                data: JSON.stringify(this),
                success: function(data) {
                    return true;
                }
            });
            return 'ok';
        }

    });

