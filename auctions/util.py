def check_bid(bid, list):
    """
    Check if the given offer is bigger than start price and previous offers
    return True or False
    """
    if float(bid) >= list.start_bid and (list.current_bid is None or float(bid) > list.current_bid):
        return True
    return False
