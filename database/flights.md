# Flights
The Flights database stores information for Airplanes, Airports, and all Flights offered (past and present) by Utopia Airlines.

ERD:
![Flights ERD](https://utopia-documentation-media.s3.amazonaws.com/database/flights.png)

### Airplane
Hibernate `Airplane`:
```java
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Airplane {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotBlank
  private String name;

  @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
  @EqualsAndHashCode.Exclude
  @ToString.Exclude
  private List<SeatConfiguration> seatConfigurations;

  public int getMaxCapacity() {
    return seatConfigurations.stream()
        .mapToInt(config -> config.getNumRows() * config.getNumSeatsPerRow())
        .sum();
  }
}
```

Hibernate `SeatConfiguration`:
```java
@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class SeatConfiguration {

  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  private Long id;

  @Enumerated(EnumType.STRING)
  private SeatClass seatClass;

  @NotNull
  private Integer numRows;

  @NotNull
  private Integer numSeatsPerRow;
}
```

## Airport
Hibernate `Airport`:
```java
@Entity
@Data
@RequiredArgsConstructor
@AllArgsConstructor
@Builder
public class Airport {

  @Id
  @NotNull
  private String iataId;

  @NotBlank
  private String name;

  @NotBlank
  private String streetAddress;

  @NotBlank
  private String city;

  @NotBlank
  private String state;

  @NotBlank
  private String zipcode;

  //Which metropolitan area does this airport service
  @ManyToOne
  private ServicingArea servicingArea;

}
```

Hibernate `ServicingArea`:
```java
@Entity
@Data
@RequiredArgsConstructor
@AllArgsConstructor
@Builder
public class ServicingArea {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotBlank
  private String areaName;
}
```

## Flights
Hibernate `Flight`:
```java
@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Flight {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private Integer possibleLoyaltyPoints;

  @ManyToOne
  private Airport origin;

  @ManyToOne
  private Airport destination;

  @OneToOne
  private Airplane airplane;

  @OneToMany(cascade = CascadeType.REMOVE)
  private List<Seat> seats;

  @Column(updatable = false)
  @CreationTimestamp
  private ZonedDateTime creationDateTime;

  private ZonedDateTime approximateDateTimeStart;

  private ZonedDateTime approximateDateTimeEnd;

  private boolean flightActive;
}
```

Hibernate `Seat`:
```java
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Seat {

  @Id
  private String id; // Flight ID, Seat Row/Col, and Class, ie "1234-2A"

  @NotNull
  private Integer seatRow;

  @NotNull
  private Character seatColumn;

  @Enumerated(EnumType.STRING)
  private SeatClass seatClass;

  @Enumerated(EnumType.STRING)
  private SeatStatus seatStatus;

  @NotNull
  private BigDecimal price;
}
```

`SeatStatus` enum:
```java
public enum SeatStatus {
  AVAILABLE,
  SOLD,
  HELD,
  BLOCKED;

  private static final List<String> stringValues = Arrays.stream(SeatStatus.values())
      .map(Enum::toString)
      .collect(Collectors.toList());

  @JsonCreator
  public static SeatStatus fromString(String text) {
    try {
      return SeatStatus.valueOf(text.toUpperCase());
    } catch (IllegalArgumentException ex) {
      throw new InvalidEnumValue(text, stringValues);
    }
  }
}
```