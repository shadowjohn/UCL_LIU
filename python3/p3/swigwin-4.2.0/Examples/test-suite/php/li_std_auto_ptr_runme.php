<?php

require "tests.php";

function checkCount($expected_count) {
    $actual_count = Klass::getTotal_count();
    check::equal($actual_count, $expected_count, "Counts incorrect");
}

# Test raw pointer handling involving virtual inheritance
$kini = new KlassInheritance("KlassInheritanceInput");
checkCount(1);
$s = useKlassRawPtr($kini);
check::equal($s, "KlassInheritanceInput", "Incorrect string: $s");
$kini = NULL;
checkCount(0);


# auto_ptr as input
$kin = new Klass("KlassInput");
checkCount(1);
$s = takeKlassAutoPtr($kin);
checkCount(0);
check::equal($s, "KlassInput", "Incorrect string: $s");
try {
    is_nullptr($kin);
    check::fail("is_nullptr check");
} catch (TypeError $e) {
}
$kin = NULL; # Should not fail, even though already deleted
checkCount(0);

$kin = new Klass("KlassInput");
checkCount(1);
$s = takeKlassAutoPtr($kin);
checkCount(0);
check::equal($s, "KlassInput", "Incorrect string: $s");
try {
    is_nullptr($kin);
    check::fail("is_nullptr check");
} catch (TypeError $e) {
}
$exception_thrown = false;
try {
  takeKlassAutoPtr($kin);
} catch (TypeError $e) {
  check::equal($e->getMessage(), "Cannot release ownership as memory is not owned for argument 1 of SWIGTYPE_p_Klass of takeKlassAutoPtr", "Unexpected exception: {$e->getMessage()}");
  $exception_thrown = true;
}
check::equal($exception_thrown, true, "double usage of takeKlassAutoPtr should have been an error");
$kin = NULL; # Should not fail, even though already deleted
checkCount(0);

$kin = new Klass("KlassInput");
$exception_thrown = false;
$notowned = get_not_owned_ptr($kin);
try {
  takeKlassAutoPtr($notowned);
} catch (TypeError $e) {
  check::equal($e->getMessage(), "Cannot release ownership as memory is not owned for argument 1 of SWIGTYPE_p_Klass of takeKlassAutoPtr", "Unexpected exception: {$e->getMessage()}");
  $exception_thrown = true;
}
check::equal($exception_thrown, true, "double usage of takeKlassAutoPtr should have been an error");
checkCount(1);
$kin = NULL;
checkCount(0);

$kini = new KlassInheritance("KlassInheritanceInput");
checkCount(1);
$s = takeKlassAutoPtr($kini);
checkCount(0);
check::equal($s, "KlassInheritanceInput", "Incorrect string: $s");
try {
    is_nullptr($kini);
    check::fail("is_nullptr check");
} catch (TypeError $e) {
}

$kini = NULL; # Should not fail, even though already deleted
checkCount(0);

takeKlassAutoPtr(NULL);
takeKlassAutoPtr(make_null());
checkCount(0);

# overloaded parameters
check::equal(overloadTest(), 0, "overloadTest failed");
check::equal(overloadTest(NULL), 1, "overloadTest failed");
check::equal(overloadTest(new Klass("over")), 1, "overloadTest failed");
checkCount(0);


# auto_ptr as output
$k1 = makeKlassAutoPtr("first");
$k2 = makeKlassAutoPtr("second");
checkCount(2);

$k1 = NULL;
checkCount(1);

check::equal($k2->getLabel(), "second", "proper label");

$k2 = NULL;
checkCount(0);

check::equal(makeNullAutoPtr(), NULL);

check::done();
