
define([
    'underscore',
    'backbone',
    'templates',
    'view/abstract/list',
    'view/abstract/list-item',
    'model/card'
], function (_, Backbone, Templates, ListView, ListItemView, CardModel) {

    var CardView = ListItemView.extend({
            template: Templates['deck-browser-card'],

            className: 'browser-result card',

            render: function () {
                ListItemView.prototype.render.apply(this, arguments);

                this.$el.data('id', this.model.id);

                return this;
            }
        }),
        Collection = Backbone.Collection.extend({

            url: function () {
                return '/api/cards/?search=' + this.search;
            },

            model: CardModel

        });

    return Backbone.View.extend({

        template: Templates['deck-browser'],

        delay: 500,

        events: {
            'keypress .search': 'keypress'
        },

        initialize: function () {
            _.bindAll(this, 'search');

            this.collection = new Collection();

            this.listView = new ListView({
                emptyMessage: '',
                collection: this.collection,
                itemView: CardView
            });
        },

        keypress: function () {
            if (this.timeout) {
                clearTimeout(this.timeout);
            }

            this.timeout = window.setTimeout(this.search, this.delay);
        },

        search: function () {
            this.collection.search = this.$search.val();
            this.collection.fetch();
        },

        render: function () {
            this.$el.html(this.template());

            this.listView.setElement(this.$('.browser-results'));
            this.listView.render();

            this.$search = this.$('.search');

            this.delegateEvents();
        }

    });

});