from GUISettings import *
from CardGUI import CardGUI
from Settings import SPADES, CLUBS, DIAMONDS


class RoundGUI:

    @staticmethod
    def create_cards_gui(cards, all_sprites):
        all_cards = pygame.sprite.Group()
        for card in cards:
            if card is not None:
                gui_card = CardGUI(card)
                all_cards.add(gui_card)
                all_sprites.add(gui_card)
        return all_cards

    @staticmethod
    def create_cards_desk(cards, all_sprites):
        all_cards = [None, None, None]
        for i in range(0, len(cards)):
            if cards[i] is not None:
                gui_card = CardGUI(cards[i])
                all_cards[i] = gui_card
                all_sprites.add(gui_card)
        return all_cards

    @staticmethod
    def display_player_cards(player_cards_gui):
        left = WIDTH / 2 - (((len(player_cards_gui) - 1) * (CARD_WIDTH + CARD_OFFSET) + CARD_WIDTH) / 2)
        for card in player_cards_gui:
            card.card.is_reversed = False
            card.left = left
            card.top = CARD_LOCATION_TOP if not card.is_clicked else CARD_LOCATION_TOP - CARD_OFFSET_TOP
            left += CARD_WIDTH + CARD_OFFSET
            card.image = card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_oponent_cards(oponent_cards_gui, left: bool):
        top = HEIGHT / 2 - float(len(oponent_cards_gui) / 2) * (CARD_WIDTH / 2)
        for card in oponent_cards_gui:
            card.card.is_reversed = True
            card.top = top
            if left:
                card.left = OPPONENT_CARD_LOCATION_LEFT
            else:
                card.left = OPPONENT_CARD_LOCATION_RIGHT
            top += CARD_WIDTH + OPPONENT_CARD_OFFSET
            card.image = card.card_back_image
            if left:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_LEFT_CARDS)
            else:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_RIGHT_CARDS)
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_bidding_cards(bidding_cards_gui, is_covered):
        left = WIDTH / 2 - float(len(bidding_cards_gui) / 2) * (CARD_WIDTH + CARD_OFFSET / 2)
        for card in bidding_cards_gui:
            card.left = left
            card.top = BIDDING_LOCATION_TOP
            left += CARD_WIDTH + CARD_OFFSET
            card.image = card.card_back_image if is_covered else card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))
            card.card.is_reversed = is_covered

    @staticmethod
    def display_desk(desk_cards_gui: [CardGUI], self_player_id):

        # gui_desk_cards = [None, None, None]

        try:
            card_gui_me = desk_cards_gui[self_player_id]
        except:
            card_gui_me = None

        try:
            card_gui_op1 = desk_cards_gui[(self_player_id + 1) % 3]
        except:
            card_gui_op1 = None

        try:
            card_gui_op2 = desk_cards_gui[(self_player_id + 2) % 3]
        except:
            card_gui_op2 = None

        top_op = 130
        top_me = 260
        left_op1 = WIDTH / 2 - 1.5 * CARD_WIDTH - 5
        left_op2 = WIDTH / 2 + 0.5 * CARD_WIDTH + 5
        left_me = WIDTH / 2 - CARD_WIDTH / 2

        if card_gui_me is not None:
            RoundGUI.display_card(card_gui_me, left_me, top_me)

        if card_gui_op1 is not None:
            RoundGUI.display_card(card_gui_op1, left_op1, top_op)

        if card_gui_op2 is not None:
            RoundGUI.display_card(card_gui_op2, left_op2, top_op)

    @staticmethod
    def display_card(card, left, top):
        if card is not None:
            card.left = left
            card.top = top
            card.image = card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top +
                                                    CARD_HEIGHT / 2))
            card.card.is_reversed = False

    @staticmethod
    def if_queen_king_pair_info(card, if_queen_king_pair, info_label, reload=False):
        if if_queen_king_pair:
            if card.color == SPADES:
                if not reload:
                    info_label.show_label("Spades Queen-King Pair + 40")
                else:
                    info_label.show_label("Last Queen-King Pair: Spades + 40")
            elif card.color == CLUBS:
                if not reload:
                    info_label.show_label("Clubs Queen-King Pair + 60")
                else:
                    info_label.show_label("Last Queen-King Pair: Clubs + 60")
            elif card.color == DIAMONDS:
                if not reload:
                    info_label.show_label("Diamonds Queen-King Pair + 80")
                else:
                    info_label.show_label("Last Queen-King Pair: Diamonds + 80")
            else:
                if not reload:
                    info_label.show_label("Heart Queen-King Pair + 100")
                else:
                    info_label.show_label("Last Queen-King Pair: Heart + 100")