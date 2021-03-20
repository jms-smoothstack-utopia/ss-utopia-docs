# User Accounts
This table stores credential information and applies to both customer users and non-customer users (employees, travel agents, administrators, etc). The `user_account` table contains information to comply with Spring `UserDetails` objects.

ERD:
![Accounts ERD](https://utopia-documentation-media.s3.amazonaws.com/database/accounts.png)

Hiberate `UserAccount`:
```java
@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class UserAccount implements UserDetails {

  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  @Column(columnDefinition = "BINARY(16)")
  private UUID id;

  @NotBlank
  @Email
  private String email;

  @ToString.Exclude
  @EqualsAndHashCode.Exclude
  @NotBlank
  private String password;

  @Builder.Default
  @Enumerated(EnumType.STRING)
  private UserRole userRole = UserRole.DEFAULT;

  @Column(updatable = false)
  @CreationTimestamp
  private ZonedDateTime creationDateTime;

  @UpdateTimestamp
  private ZonedDateTime lastModifiedDateTime;

  @Builder.Default
  private boolean accountNonExpired = true;
  @Builder.Default
  private boolean accountNonLocked = true;
  @Builder.Default
  private boolean credentialsNonExpired = true;
  @Builder.Default
  private boolean enabled = true;
  @Builder.Default
  private boolean confirmed = false;

  public Collection<? extends GrantedAuthority> getAuthorities() {
    if (userRole == null) {
      return Collections.emptySet();
    }
    return Set.of(new SimpleGrantedAuthority(userRole.getRole()));
  }

  @Override
  public String getUsername() {
    return email;
  }

}
```

`UserRole` enum*:
```java
public enum UserRole {
  DEFAULT("ROLE_DEFAULT"),
  CUSTOMER("ROLE_CUSTOMER"),
  TRAVEL_AGENT("ROLE_TRAVEL_AGENT"),
  EMPLOYEE("ROLE_EMPLOYEE"),
  ADMIN("ROLE_ADMIN"),
  SERVICE("ROLE_SERVICE");

  private final String roleName;

  UserRole(String roleName) {
    this.roleName = roleName;
  }

  public String getRole() {
    return roleName;
  }

  public String getRoleName() {
    return roleName.replace("ROLE_", "");
  }
}
```

*_`UserRole` is used to create `SimpleGrantedAuthority` with Spring Security. It is currently under review for refactoring to allow for better segregation of duties._

Hibernate `AccountActionToken`:
```java
@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class AccountActionToken {

  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  @Column(columnDefinition = "BINARY(16)")
  private UUID token;

  @NotNull
  @Column(columnDefinition = "BINARY(16)")
  private UUID ownerAccountId;

  @NotNull
  @Enumerated(EnumType.STRING)
  private AccountAction action;

  @Column(updatable = false)
  @CreationTimestamp
  private ZonedDateTime creation;

  @Builder.Default
  private boolean active = true;

}
```

`AccountAction` enum:
```java
public enum AccountAction {
  PASSWORD_RESET(10), // 10 minutes
  CONFIRMATION(60), // 1 hour
  DELETION(10); // 10 minutes

  private final int minutesToLive;

  AccountAction(int minutesToLive) {
    this.minutesToLive = minutesToLive;
  }

  public int getMinutesToLive() {
    return minutesToLive;
  }
}
```

Hibernate `PasswordReset`*:
```java
@Data
@Entity
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PasswordReset {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(columnDefinition = "BINARY(16)")
  private UUID userId;

  private String email;

  @Column(unique = true)
  private String token;

  @Column(updatable = false)
  @CreationTimestamp
  private ZonedDateTime creation;

  @Builder.Default
  private boolean isActive = true;
}
```

*_The `PasswordReset` class shares fields and the functionality of the `AccountActionToken` and is considered technical debt at this time. It is to be refactored in future sprints to reduce code duplication._