
define(['underscore','backbone', 'view/abstract/list-item'],
function (_, Backbone, ListItemView) {

    return Backbone.View.extend({

        initialize: function (options) {
            this.views = {};

            this.itemView = options.itemView || ListItemView;
            this.itemOptions = options.itemOptions || {};
            this.emptyMessage = _.isUndefined(options.emptyMessage) ?
                'This list is empty.' : options.emptyMessage;

            _.bindAll(this, 'render');

            this.setCollection(options.collection);
        },

        setCollection: function (collection) {
            if (!(collection instanceof Backbone.Collection)) {
                collection = new Backbone.Collection(collection);
            }

            if (!_.isUndefined(this.collection)) {
                this.stopListening(this.collection);
                this.views = {};
            }

            if (!_.isUndefined(collection)) {
                this.collection = collection;
                this.listenTo(this.collection, 'add remove reset sort',
                    this.render);
            }
        },

        render: function () {
            var collection, list, count = 0;

            if (!_.isUndefined(this.collection)) {
                this.$el.empty();

                if (this.collection.length) {

                    list = document.createDocumentFragment();

                    this.collection.each(function (item) {
                        var id = item.id || item.cid,
                            view = this.views[id];

                        if (_.isUndefined(view)) {
                            view = new this.itemView(
                                _.extend({ model: item }, this.itemOptions)
                            );
                            this.views[id] = view;
                        }

                        count++;
                        list.appendChild(view.render().el);
                    }, this);

                    this.$el.append(list);
                } else {
                    this.$el.html(this.emptyMessage);
                }
            }

            return this;
        }

    });

});