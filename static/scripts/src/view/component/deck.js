

define([
    'underscore',
    'backbone',
    'templates',
    'view/abstract/list',
    'view/abstract/list-item',
    'view/component/confirm',

    'backbone.stickit'
], function (_, Backbone, Templates, ListView, ListItemView, Confirm) {

    var CardView = ListItemView.extend({
            template: Templates['deck-content-card'],

            className: 'deck-card card',

            render: function () {
                ListItemView.prototype.render.apply(this, arguments);

                this.$el.data('id', this.model.get('card.id'));

                return this;
            }
        }),
        MainCollectionView = ListView.extend({

            render: function () {
                ListView.prototype.render.apply(this, arguments);

                if (this.collection.length > 48) {
                    this.$el.addClass('xs');
                } else if (this.collection.length > 40) {
                    this.$el.addClass('small');
                } else {
                    this.$el.removeClass('small').removeClass('xs');
                }

                return this;
            }
        });

    return Backbone.View.extend({

        template: Templates['deck-content'],

        events: {
            'click .save': 'save',
            'click .delete': 'delete'
        },

        stickit: {
            '.deck-name': 'name'
        },

        initialize: function () {

            _.bindAll(this, 'render');

            this.mainView = new MainCollectionView({
                emptyMessage: '',
                itemView: CardView
            });

            this.extraView = new ListView({
                emptyMessage: '',
                itemView: CardView
            });

            this.sideView = new ListView({
                emptyMessage: '',
                itemView: CardView
            });
        },

        render: function () {

            this.$el.empty().html(this.template(this.model.attributes));

            // this.$deckName = this.$('.deck-name');
            // this.$nameForm = this.$('.form-name');

            this.mainView.setElement(this.$('.deck-main'));
            this.mainView.setCollection(this.model.get('deck_cards_main'));
            this.mainView.render();

            this.extraView.setElement(this.$('.deck-extra'));
            this.extraView.setCollection(this.model.get('deck_cards_extra'));
            this.extraView.render();

            this.sideView.setElement(this.$('.deck-side'));
            this.sideView.setCollection(this.model.get('deck_cards_side'));
            this.sideView.render();

            this.delegateEvents();

            this.listenTo(this.model, 'change', this.render);

            return this;
        },

        save: function () {
            this.model.save();
        },

        delete: function () {
            Confirm.ask().done(_.bind(function () {
                this.model.destroy();
            }, this));
        },

    });

});