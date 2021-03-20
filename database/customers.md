## Customer Records
This table stores customer-specific account information including address, contact methods, and payment methods.

ERD:
![Customers ERD](https://utopia-documentation-media.s3.amazonaws.com/database/customers.png)

Hibernate `Customer`:
```java
@Data
@Entity
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Customer {

  @Id
  @Column(columnDefinition = "BINARY(16)")
  private UUID id;

  private String firstName;

  private String lastName;

  @Builder.Default
  private Integer loyaltyPoints = 0;

  private String phoneNumber;

  @Column(unique = true)
  private String email;

  @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
  private Set<Address> addresses;

  @Builder.Default
  private Boolean ticketEmails = true;

  @Builder.Default
  private Boolean flightEmails = true;

  @EqualsAndHashCode.Exclude
  @ToString.Exclude
  @OneToMany(cascade = CascadeType.ALL)
  private Set<PaymentMethod> paymentMethods;
}
```

Hibernate `Address`*:
```java
@Data
@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Address {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private Integer cardinality;

  private String line1;

  private String line2;

  private String city;

  private String state;

  private String zipcode;
}
```

*_`Address` is slated for refactorization in future sprints to comply with data requirements._

Hibernate `PaymentMethod`*:
```java
@Data
@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class PaymentMethod {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotNull
  private UUID ownerId;

  @NotNull
  private String accountNum;

  private String notes;

}
```

*_`PaymentMethod` is a prototype and will likely be significantly factored or replaced entirely once payment integration is initiated in future sprints._