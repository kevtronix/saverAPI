from api.models import Ticket, ShelterRequest

def match_checked_tickets_with_requests():
    for request in ShelterRequest.objects.filter(fulfilled=False):
        remaining_quantity = request.quantity_requested

        # Find tickets that match the food category and have some quantity
        matching_tickets = Ticket.objects.filter(
            food_category=request.food_category, 
            quantity__gt=0,  # Tickets with some quantity
            checked=True
        ).order_by('-quantity')  # Optional: Order by quantity to use bigger tickets first

        for ticket in matching_tickets:
            if remaining_quantity <= 0:
                break  # Request is fully fulfilled

            if ticket.quantity <= remaining_quantity:
                # Ticket can partially (or fully) fulfill the request
                remaining_quantity -= ticket.quantity
                ticket.quantity = 0
                ticket.save()
                request.tickets.add(ticket)  # Assuming a many-to-many relationship
            else:
                # Ticket can fulfill more than the remaining quantity
                ticket.quantity -= remaining_quantity
                ticket.save()
                request.tickets.add(ticket)
                remaining_quantity = 0

        if remaining_quantity <= 0:
            request.fulfilled = True
            request.save()
