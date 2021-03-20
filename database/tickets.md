# Tickets
The Ticket table stores information about purchased tickets only.

ERD:
![Tickets ERD](https://utopia-documentation-media.s3.amazonaws.com/database/tickets.png)

Hibernate `Ticket`:
```java
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Ticket {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotNull
  private Long flightId;

  @NotNull
  private ZonedDateTime flightTime;

  @NotNull
  private UUID purchaserId;

  @NotBlank
  private String passengerName;

  @NotBlank
  private String seatClass;

  @NotBlank
  private String seatNumber;

  @NotNull
  private TicketStatus status;

  public enum TicketStatus {
    PURCHASED,
    CHECKED_IN,
    CANCELLED,
    REFUNDED;

    TicketStatus fromString(String ticketStatus) {
      return TicketStatus.valueOf(ticketStatus.toUpperCase());
    }
  }
}
```