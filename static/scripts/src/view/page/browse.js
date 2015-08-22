

define([
    'view/abstract/page-list',
    'view/table/link-cell',
    'view/table/price-cell',
    'view/table/counter-cell',
    'collection/card-version',
    'view/table/price-shift-cell'
], function (PageListView, LinkCell, PriceCell, CounterCell,
        CardVersionCollection, PriceShiftCell) {

    var rootUrl = '/browse/',
        CardLinkCell = LinkCell(rootUrl, 'card.identifier');

    return PageListView.extend({

        el: '#content.page-browse',

        gridColumns: [
            {
                name: 'user_card_version.have_count',
                label: 'Have',
                editable: false,
                cell: CounterCell
            },
            {
                name: 'set_number',
                label: 'Set Number',
                editable: false,
                cell: CardLinkCell
            },
            {
                name: 'card.name',
                label: 'Name',
                editable: false,
                cell: CardLinkCell
            },
            {
                name: 'card_set.name',
                label: 'Card Set',
                editable: false,
                cell: 'string'
            },
            {
                name: 'card.card_type.name',
                label: 'Type',
                editable: false,
                cell: 'string'
            },
            {
                name: 'rarity.name',
                label: 'Rarity',
                editable: false,
                cell: 'string'
            },
            {
                name: 'price_shift',
                label: 'Shift',
                editable: false,
                cell: PriceShiftCell
            },
            {
                name: 'price_low',
                label: 'Low',
                editable: false,
                cell: PriceCell
            },
            {
                name: 'price_avg',
                label: 'Avg',
                editable: false,
                cell: PriceCell
            },
            {
                name: 'price_high',
                label: 'High',
                editable: false,
                cell: PriceCell
            }
        ],

        rootUrl: rootUrl,

        initialize: function () {
            this.collection = new (CardVersionCollection('/api/browse/'))();

            PageListView.prototype.initialize.apply(this, arguments);
        }

    });

});